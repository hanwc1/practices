'use strict';

/* ================= 상수 / 설정 ================= */

const STORAGE_KEY = 'schedule-app.events.v1';
const UPCOMING_DAYS = 7;
const MAX_CHIPS = 3;

const CATEGORIES = {
  work: { label: '업무', color: 'var(--cat-work)' },
  personal: { label: '개인', color: 'var(--cat-personal)' },
  important: { label: '중요', color: 'var(--cat-important)' },
  etc: { label: '기타', color: 'var(--cat-etc)' },
};

const REPEAT_LABELS = {
  none: '',
  daily: '매일',
  weekly: '매주',
  monthly: '매월',
  yearly: '매년',
};

const WEEKDAY_NAMES = ['일', '월', '화', '수', '목', '금', '토'];

/* ================= 날짜 유틸 ================= */

const pad = (n) => String(n).padStart(2, '0');

/** Date -> 'YYYY-MM-DD' (로컬 시간 기준) */
function toKey(d) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

/** 'YYYY-MM-DD' -> Date (로컬 자정) */
function parseKey(key) {
  const [y, m, d] = key.split('-').map(Number);
  return new Date(y, m - 1, d);
}

function addDays(d, n) {
  const r = new Date(d);
  r.setDate(r.getDate() + n);
  return r;
}

function todayKey() {
  return toKey(new Date());
}

function formatDayTitle(key) {
  const d = parseKey(key);
  return `${d.getMonth() + 1}월 ${d.getDate()}일 (${WEEKDAY_NAMES[d.getDay()]})`;
}

function relativeLabel(key) {
  const diff = Math.round((parseKey(key) - parseKey(todayKey())) / 86400000);
  if (diff === 0) return '오늘';
  if (diff === 1) return '내일';
  if (diff === 2) return '모레';
  return '';
}

/* ================= 저장소 ================= */

function isValidEvent(e) {
  return (
    e && typeof e === 'object' &&
    typeof e.id === 'string' &&
    typeof e.title === 'string' && e.title.trim() !== '' &&
    typeof e.date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(e.date)
  );
}

function normalizeEvent(e) {
  return {
    id: e.id,
    title: e.title.trim(),
    date: e.date,
    allDay: Boolean(e.allDay),
    start: typeof e.start === 'string' ? e.start : '',
    end: typeof e.end === 'string' ? e.end : '',
    category: CATEGORIES[e.category] ? e.category : 'etc',
    repeat: REPEAT_LABELS[e.repeat] !== undefined ? e.repeat : 'none',
    repeatUntil: typeof e.repeatUntil === 'string' ? e.repeatUntil : '',
    memo: typeof e.memo === 'string' ? e.memo : '',
  };
}

function loadEvents() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.filter(isValidEvent).map(normalizeEvent) : [];
  } catch (err) {
    console.warn('일정 불러오기 실패:', err);
    return [];
  }
}

function saveEvents() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(events));
  } catch (err) {
    alert('일정을 저장하지 못했습니다. 브라우저 저장소 설정을 확인해 주세요.');
    console.error(err);
  }
}

function newId() {
  if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

/* ================= 반복 일정 계산 ================= */

/** 해당 날짜(key)에 이 일정이 발생하는지 여부 */
function occursOn(ev, key) {
  if (key < ev.date) return false;
  if (ev.repeat !== 'none' && ev.repeatUntil && key > ev.repeatUntil) return false;

  const start = parseKey(ev.date);
  const day = parseKey(key);

  switch (ev.repeat) {
    case 'none':
      return key === ev.date;
    case 'daily':
      return true;
    case 'weekly':
      return day.getDay() === start.getDay();
    case 'monthly':
      return day.getDate() === start.getDate();
    case 'yearly':
      return day.getMonth() === start.getMonth() && day.getDate() === start.getDate();
    default:
      return false;
  }
}

function compareEvents(a, b) {
  if (a.allDay !== b.allDay) return a.allDay ? -1 : 1;
  const t = (a.start || '').localeCompare(b.start || '');
  return t !== 0 ? t : a.title.localeCompare(b.title, 'ko');
}

function eventsOn(key) {
  return events.filter((ev) => occursOn(ev, key)).sort(compareEvents);
}

/* ================= 상태 ================= */

let events = loadEvents();
let selectedKey = todayKey();
let viewYear = parseKey(selectedKey).getFullYear();
let viewMonth = parseKey(selectedKey).getMonth(); // 0-11
let editingId = null;
let searchQuery = '';

/* ================= DOM 헬퍼 ================= */

const $ = (sel) => document.querySelector(sel);

/** 안전한 요소 생성 (텍스트는 항상 textContent 로 넣어 XSS 방지) */
function el(tag, props = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (k === 'class') node.className = v;
    else if (k === 'style') Object.assign(node.style, v);
    else if (k.startsWith('on')) node.addEventListener(k.slice(2), v);
    else if (k === 'text') node.textContent = v;
    else node.setAttribute(k, v);
  }
  for (const c of children) {
    if (c == null || c === false) continue;
    node.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return node;
}

function timeText(ev) {
  if (ev.allDay) return '하루 종일';
  if (ev.start && ev.end) return `${ev.start} – ${ev.end}`;
  return ev.start || ev.end || '';
}

/* ================= 렌더링 ================= */

function renderCalendar() {
  $('#cal-title').textContent = `${viewYear}년 ${viewMonth + 1}월`;

  const grid = $('#cal-grid');
  grid.replaceChildren();

  const first = new Date(viewYear, viewMonth, 1);
  const gridStart = addDays(first, -first.getDay());
  const today = todayKey();

  for (let i = 0; i < 42; i++) {
    const date = addDays(gridStart, i);
    const key = toKey(date);
    const dayEvents = eventsOn(key);

    const classes = ['day'];
    if (date.getMonth() !== viewMonth) classes.push('other-month');
    if (date.getDay() === 0) classes.push('sun');
    if (date.getDay() === 6) classes.push('sat');
    if (key === today) classes.push('today');
    if (key === selectedKey) classes.push('selected');

    const cell = el('div', {
      class: classes.join(' '),
      tabindex: '0',
      role: 'button',
      'aria-label': `${formatDayTitle(key)}, 일정 ${dayEvents.length}개`,
      'data-key': key,
    }, el('span', { class: 'day-num', text: date.getDate() }));

    dayEvents.slice(0, MAX_CHIPS).forEach((ev) => {
      const chip = el('div', {
        class: ev.allDay ? 'chip' : 'chip timed',
        title: `${timeText(ev)} ${ev.title}`.trim(),
        text: ev.allDay ? ev.title : `${ev.start ? ev.start + ' ' : ''}${ev.title}`,
      });
      chip.style.setProperty('--chip-color', CATEGORIES[ev.category].color);
      cell.append(chip);
    });
    if (dayEvents.length > MAX_CHIPS) {
      cell.append(el('div', { class: 'more', text: `+${dayEvents.length - MAX_CHIPS}개 더` }));
    }

    grid.append(cell);
  }
}

function eventItem(ev, { showDate = null } = {}) {
  const metaParts = [CATEGORIES[ev.category].label];
  if (ev.repeat !== 'none') {
    metaParts.push(`🔁 ${REPEAT_LABELS[ev.repeat]}${ev.repeatUntil ? ` (~${ev.repeatUntil})` : ''}`);
  }
  if (showDate) metaParts.unshift(showDate);

  const li = el('li', {
    class: 'event-item',
    tabindex: '0',
    role: 'button',
    'aria-label': `${ev.title} 수정`,
    onclick: () => openDialog(ev.id),
    onkeydown: (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDialog(ev.id); }
    },
  },
    el('div', { class: 'time', text: timeText(ev) }),
    el('div', { class: 'body' },
      el('div', { class: 'title', text: ev.title }),
      el('div', { class: 'meta', text: metaParts.join(' · ') }),
      ev.memo ? el('div', { class: 'memo', text: ev.memo }) : null,
    ),
  );
  li.style.setProperty('--chip-color', CATEGORIES[ev.category].color);
  return li;
}

function renderDayPanel() {
  const rel = relativeLabel(selectedKey);
  $('#day-title').textContent = formatDayTitle(selectedKey) + (rel ? ` · ${rel}` : '');

  const list = $('#day-list');
  list.replaceChildren();
  const dayEvents = eventsOn(selectedKey);
  if (dayEvents.length === 0) {
    list.append(el('li', { class: 'empty', text: '일정이 없습니다.' }));
  } else {
    dayEvents.forEach((ev) => list.append(eventItem(ev)));
  }
}

function renderSidePanel() {
  const list = $('#upcoming-list');
  list.replaceChildren();

  if (searchQuery) {
    $('#side-title').textContent = `검색 결과: “${searchQuery}”`;
    const q = searchQuery.toLowerCase();
    const found = events
      .filter((ev) => ev.title.toLowerCase().includes(q) || ev.memo.toLowerCase().includes(q))
      .sort((a, b) => a.date.localeCompare(b.date) || compareEvents(a, b));
    if (found.length === 0) {
      list.append(el('li', { class: 'empty', text: '검색 결과가 없습니다.' }));
    }
    found.forEach((ev) => list.append(eventItem(ev, { showDate: ev.date })));
    return;
  }

  $('#side-title').textContent = `다가오는 일정 (${UPCOMING_DAYS}일)`;
  const start = parseKey(todayKey());
  let total = 0;
  for (let i = 0; i < UPCOMING_DAYS; i++) {
    const key = toKey(addDays(start, i));
    const dayEvents = eventsOn(key);
    if (dayEvents.length === 0) continue;
    total += dayEvents.length;
    const rel = relativeLabel(key);
    list.append(el('li', { class: 'group-label', text: formatDayTitle(key) + (rel ? ` · ${rel}` : '') }));
    dayEvents.forEach((ev) => list.append(eventItem(ev)));
  }
  if (total === 0) {
    list.append(el('li', { class: 'empty', text: '앞으로 7일간 일정이 없습니다.' }));
  }
}

function renderLegend() {
  const legend = $('#legend');
  legend.replaceChildren();
  for (const cat of Object.values(CATEGORIES)) {
    const s = el('span', { text: cat.label });
    s.style.setProperty('--chip-color', cat.color);
    legend.append(s);
  }
}

function render() {
  renderCalendar();
  renderDayPanel();
  renderSidePanel();
}

/* ================= 일정 편집 다이얼로그 ================= */

const dialog = $('#event-dialog');
const form = $('#event-form');
const F = form.elements;

function syncFormState() {
  const allDay = F.allDay.checked;
  $('.time-row').classList.toggle('disabled', allDay);
  F.start.disabled = allDay;
  F.end.disabled = allDay;
  $('.repeat-until').hidden = F.repeat.value === 'none';
}

function openDialog(id = null, dateKey = selectedKey) {
  editingId = id;
  const ev = id ? events.find((e) => e.id === id) : null;
  $('#form-error').textContent = '';

  form.reset();
  if (ev) {
    $('#dialog-title').textContent = '일정 수정';
    F.title.value = ev.title;
    F.date.value = ev.date;
    F.allDay.checked = ev.allDay;
    F.start.value = ev.start;
    F.end.value = ev.end;
    F.category.value = ev.category;
    F.repeat.value = ev.repeat;
    F.repeatUntil.value = ev.repeatUntil;
    F.memo.value = ev.memo;
  } else {
    $('#dialog-title').textContent = '새 일정';
    F.date.value = dateKey;
    F.start.value = '09:00';
    F.end.value = '10:00';
    F.category.value = 'work';
    F.repeat.value = 'none';
  }
  $('#btn-delete').hidden = !ev;
  syncFormState();
  dialog.showModal();
  F.title.focus();
}

function closeDialog() {
  dialog.close();
  editingId = null;
}

function readForm() {
  const data = {
    title: F.title.value.trim(),
    date: F.date.value,
    allDay: F.allDay.checked,
    start: F.allDay.checked ? '' : F.start.value,
    end: F.allDay.checked ? '' : F.end.value,
    category: F.category.value,
    repeat: F.repeat.value,
    repeatUntil: F.repeat.value === 'none' ? '' : F.repeatUntil.value,
    memo: F.memo.value.trim(),
  };

  if (!data.title) return { error: '제목을 입력해 주세요.' };
  if (!data.date) return { error: '날짜를 선택해 주세요.' };
  if (!data.allDay && data.start && data.end && data.end < data.start) {
    return { error: '종료 시간은 시작 시간보다 늦어야 합니다.' };
  }
  if (data.repeatUntil && data.repeatUntil < data.date) {
    return { error: '반복 종료일은 시작 날짜 이후여야 합니다.' };
  }
  return { data };
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const { data, error } = readForm();
  if (error) {
    $('#form-error').textContent = error;
    return;
  }

  if (editingId) {
    const idx = events.findIndex((ev) => ev.id === editingId);
    if (idx !== -1) events[idx] = { ...events[idx], ...data };
  } else {
    events.push({ id: newId(), ...data });
  }
  saveEvents();

  // 저장한 날짜로 이동해서 바로 확인할 수 있게
  selectedKey = data.date;
  const d = parseKey(data.date);
  viewYear = d.getFullYear();
  viewMonth = d.getMonth();

  closeDialog();
  render();
});

$('#btn-delete').addEventListener('click', () => {
  const ev = events.find((x) => x.id === editingId);
  if (!ev) return;
  const msg = ev.repeat !== 'none'
    ? `반복 일정 “${ev.title}”의 모든 반복을 삭제할까요?`
    : `“${ev.title}” 일정을 삭제할까요?`;
  if (!confirm(msg)) return;
  events = events.filter((x) => x.id !== editingId);
  saveEvents();
  closeDialog();
  render();
});

$('#btn-cancel').addEventListener('click', closeDialog);
F.allDay.addEventListener('change', syncFormState);
F.repeat.addEventListener('change', syncFormState);
// 배경(backdrop) 클릭 시 닫기
dialog.addEventListener('click', (e) => {
  if (e.target === dialog) closeDialog();
});

/* ================= 내보내기 / 가져오기 ================= */

function exportJSON() {
  const blob = new Blob([JSON.stringify(events, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = el('a', { href: url, download: `schedule-${todayKey()}.json` });
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function importJSON(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const parsed = JSON.parse(reader.result);
      if (!Array.isArray(parsed)) throw new Error('배열 형식이 아닙니다.');
      const valid = parsed.filter(isValidEvent).map(normalizeEvent);
      if (valid.length === 0) throw new Error('가져올 수 있는 일정이 없습니다.');

      const replace = events.length > 0 && confirm(
        `${valid.length}개 일정을 가져옵니다.\n\n[확인] 기존 일정을 모두 바꾸기\n[취소] 기존 일정에 합치기`
      );
      if (replace) {
        events = valid;
      } else {
        const ids = new Set(events.map((e) => e.id));
        events = events.concat(valid.filter((e) => !ids.has(e.id)));
      }
      saveEvents();
      render();
      alert(`${valid.length}개 일정을 가져왔습니다.`);
    } catch (err) {
      alert(`가져오기 실패: ${err.message}`);
    }
  };
  reader.readAsText(file);
}

/* ================= 이벤트 바인딩 ================= */

function goMonth(delta) {
  const d = new Date(viewYear, viewMonth + delta, 1);
  viewYear = d.getFullYear();
  viewMonth = d.getMonth();
  renderCalendar();
}

function goToday() {
  selectedKey = todayKey();
  const d = parseKey(selectedKey);
  viewYear = d.getFullYear();
  viewMonth = d.getMonth();
  render();
}

function selectDay(key) {
  selectedKey = key;
  const d = parseKey(key);
  if (d.getFullYear() !== viewYear || d.getMonth() !== viewMonth) {
    viewYear = d.getFullYear();
    viewMonth = d.getMonth();
  }
  renderCalendar();
  renderDayPanel();
}

$('#btn-prev').addEventListener('click', () => goMonth(-1));
$('#btn-next').addEventListener('click', () => goMonth(1));
$('#btn-today').addEventListener('click', goToday);
$('#btn-add').addEventListener('click', () => openDialog(null, selectedKey));
$('#btn-add-day').addEventListener('click', () => openDialog(null, selectedKey));

const grid = $('#cal-grid');
grid.addEventListener('click', (e) => {
  const cell = e.target.closest('.day');
  if (cell) selectDay(cell.dataset.key);
});
grid.addEventListener('dblclick', (e) => {
  const cell = e.target.closest('.day');
  if (cell) openDialog(null, cell.dataset.key);
});
grid.addEventListener('keydown', (e) => {
  const cell = e.target.closest('.day');
  if (!cell) return;
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    selectDay(cell.dataset.key);
    return;
  }
  const moves = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 };
  if (moves[e.key] !== undefined) {
    e.preventDefault();
    const next = toKey(addDays(parseKey(cell.dataset.key), moves[e.key]));
    selectDay(next);
    grid.querySelector(`[data-key="${next}"]`)?.focus();
  }
});

let searchTimer;
$('#search').addEventListener('input', (e) => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    searchQuery = e.target.value.trim();
    renderSidePanel();
  }, 150);
});

// 메뉴
const menuBtn = $('#btn-menu');
const menuList = $('#menu-list');
function setMenu(open) {
  menuList.hidden = !open;
  menuBtn.setAttribute('aria-expanded', String(open));
}
menuBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  setMenu(menuList.hidden);
});
document.addEventListener('click', (e) => {
  if (!menuList.hidden && !e.target.closest('.menu')) setMenu(false);
});
$('#btn-export').addEventListener('click', () => { setMenu(false); exportJSON(); });
$('#btn-import').addEventListener('click', () => { setMenu(false); $('#import-file').click(); });
$('#import-file').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) importJSON(file);
  e.target.value = '';
});
$('#btn-clear').addEventListener('click', () => {
  setMenu(false);
  if (events.length === 0) return;
  if (!confirm(`모든 일정(${events.length}개)을 삭제할까요? 되돌릴 수 없습니다.`)) return;
  events = [];
  saveEvents();
  render();
});

// 다른 탭에서 변경되면 동기화
window.addEventListener('storage', (e) => {
  if (e.key === STORAGE_KEY) {
    events = loadEvents();
    render();
  }
});

// 단축키: N = 새 일정, T = 오늘
document.addEventListener('keydown', (e) => {
  if (dialog.open || e.metaKey || e.ctrlKey || e.altKey) return;
  if (e.target.matches('input, textarea, select')) return;
  if (e.key === 'n' || e.key === 'N') { e.preventDefault(); openDialog(null, selectedKey); }
  if (e.key === 't' || e.key === 'T') { e.preventDefault(); goToday(); }
});

/* ================= 초기화 ================= */

(function init() {
  const select = F.category;
  for (const [value, cat] of Object.entries(CATEGORIES)) {
    select.append(el('option', { value, text: cat.label }));
  }
  renderLegend();
  render();
})();
