const DATA = './data';
const ART = './public';
const app = document.querySelector('#app');

const [sceneData, characterData, choiceData, vocabularyData, quizData] = await Promise.all([
  fetch(`${DATA}/scenes.json`).then(readJson),
  fetch(`${DATA}/characters.json`).then(readJson),
  fetch(`${DATA}/choices.json`).then(readJson),
  fetch(`${DATA}/vocabulary.json`).then(readJson),
  fetch(`${DATA}/quiz.json`).then(readJson),
]);
const scenes = sceneData.scenes;
const characters = Object.fromEntries(characterData.characters.map((item) => [item.characterId, item]));
const choices = Object.fromEntries(choiceData.choices.map((item) => [item.choiceId, item]));
const vocabulary = vocabularyData.vocabulary;
const quiz = quizData.questions;
const names = { narrator: 'ผู้เล่าเรื่อง' };
for (const character of Object.values(characters)) names[character.characterId] = character.thaiName;

const state = {
  screen: 'menu',
  sceneIndex: Number(localStorage.getItem('plai-ngam-scene') || 0),
  lineIndex: Number(localStorage.getItem('plai-ngam-line') || 0),
  score: Number(localStorage.getItem('plai-ngam-score') || 0),
  answered: JSON.parse(localStorage.getItem('plai-ngam-answered') || '{}'),
  quizIndex: Number(localStorage.getItem('plai-ngam-quiz-index') || 0),
  quizAnswers: JSON.parse(localStorage.getItem('plai-ngam-quiz-answers') || '{}'),
  quizScore: Number(localStorage.getItem('plai-ngam-quiz-score') || 0),
  choiceAnswer: null,
  drawer: null,
};
state.sceneIndex = Math.min(Math.max(0, state.sceneIndex), scenes.length - 1);

function readJson(response) {
  if (!response.ok) throw new Error('อ่านข้อมูลโครงการไม่สำเร็จ');
  return response.json();
}
function esc(value = '') {
  return String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
}
function image(path) { return new URL(`${ART}/${path}`, document.baseURI).href; }
function currentScene() { return scenes[state.sceneIndex]; }
function currentDialogue() { return currentScene().dialogues[state.lineIndex]; }
function sceneNumber(scene = currentScene()) { return String(scene.sceneOrder).padStart(2, '0'); }

function renderMenu() {
  state.screen = 'menu';
  const saved = localStorage.getItem('plai-ngam-scene') !== null;
  app.innerHTML = `
    <section class="title-screen" style="--menu-art:url('${image('assets/backgrounds/main_menu/bg_main_menu.webp')}')">
      <header class="topbar title-topbar"><span class="seal-mark">พล</span><span>วรรณคดีไทย · เรื่องเล่าแบบมีส่วนร่วม</span><button class="icon-button" data-action="vocabulary" aria-label="เปิดคลังคำศัพท์">ก</button></header>
      <div class="title-composition"><div class="title-copy">
        <p class="title-kicker">ขุนช้างขุนแผน · ตอนกำเนิดพลายงาม</p>
        <h1>พลายงาม<br /><span>กำเนิดแห่งชะตา</span></h1>
        <p class="title-intro">เรื่องของเด็กคนหนึ่งที่ต้องออกเดินทาง<br class="desktop-break" />เพื่อค้นหาความจริงและบ้านที่รอเขาอยู่</p>
        <div class="title-actions"><button class="button button-primary" data-action="start">${saved ? 'เริ่มเรื่องต่อ' : 'เริ่มเรื่อง'}</button><button class="button button-quiet" data-action="chapters">เลือกฉาก</button></div>
        <p class="title-footnote">8 ฉาก · บทสนทนาและคำถามชวนคิด</p>
      </div><div class="chapter-stamp" aria-hidden="true"><span>เสภา</span><strong>พลาย<br />งาม</strong><small>บทเรียนรู้</small></div></div>
      <footer class="title-footer"><span>เรียบเรียงเพื่อการเรียนรู้</span><span>เลื่อนผ่านเรื่องราวตามจังหวะของคุณ</span></footer>
      ${state.drawer === 'chapters' ? renderChapterDrawer() : ''}${state.drawer === 'vocabulary' ? renderVocabularyDrawer() : ''}
    </section>`;
}

function renderChapterDrawer() {
  return `<div class="drawer-backdrop" data-action="close-drawer"><section class="chapter-drawer" data-action="none" aria-label="เลือกฉาก"><div class="drawer-heading"><div><small>สารบัญ</small><h2>เลือกฉาก</h2></div><button class="icon-button" data-action="close-drawer" aria-label="ปิด">×</button></div><div class="chapter-list">${scenes.map((scene, index) => `<button class="chapter-link" data-action="go-scene" data-index="${index}"><span class="chapter-index">${sceneNumber(scene)}</span><span><strong>${esc(scene.title)}</strong><small>${esc(scene.summary)}</small></span><span class="chapter-time">${scene.estimatedReadingMinutes} นาที</span></button>`).join('')}</div></section></div>`;
}
function renderVocabularyDrawer() {
  return `<div class="drawer-backdrop" data-action="close-drawer"><section class="chapter-drawer vocabulary-drawer" data-action="none" aria-label="คลังคำศัพท์"><div class="drawer-heading"><div><small>อ่านเรื่องให้ลึกขึ้น</small><h2>คลังคำศัพท์</h2></div><button class="icon-button" data-action="close-drawer" aria-label="ปิด">×</button></div><div class="vocabulary-list">${vocabulary.map((word) => `<article class="word-entry"><div><h3>${esc(word.word)}</h3><span>${esc(word.pronunciation)}</span></div><p>${esc(word.meaning)}</p><small>${esc(word.contextualMeaning)}</small></article>`).join('')}</div></section></div>`;
}

function renderStage(scene, dialogue) {
  const speaker = dialogue?.speaker;
  const backgroundPath = scene.backgroundPath || `assets/backgrounds/scenes/${scene.background}.webp`;
  const featuredPath = scene.eventCG ? `assets/backgrounds/cg/${scene.eventCG}.webp` : backgroundPath;
  const showSprites = !scene.eventCG && scene.sceneId !== 'scene06';
  const actorIds = scene.characters.filter((id) => id !== 'phlai_ngam' || scene.sceneOrder > 1);
  const actorLayout = actorIds.length === 2 ? 'two-actors' : actorIds.length === 1 ? 'one-actor' : 'three-actors';
  return `<div class="scene-art ${scene.eventCG ? 'has-event-cg' : ''}">
    <img class="scene-backdrop" src="${image(featuredPath)}" alt="" aria-hidden="true" />
    ${scene.eventCG
      ? `<img class="scene-image event-cg" src="${image(featuredPath)}" alt="ภาพเหตุการณ์: ${esc(scene.title)}" />`
      : `<img class="scene-image background-image" src="${image(backgroundPath)}" alt="ฉากหลัง: ${esc(scene.title)}" />`}
    <div class="scene-tint"></div>
    <div class="scene-topline"><button class="icon-button glass-button" data-action="menu" aria-label="กลับหน้าแรก">⌂</button><div class="scene-caption"><span>ฉาก ${sceneNumber(scene)} / 08</span><strong>${esc(scene.title)}</strong></div><button class="icon-button glass-button" data-action="vocabulary" aria-label="เปิดคลังคำศัพท์">ก</button></div>
    ${showSprites ? `<div class="character-stage ${actorLayout}">${actorIds.map((id, index, actors) => {
      const character = characters[id];
      const expression = scene.expressions?.[id] || 'normal';
      const path = character?.spriteAssets?.[expression] || character?.spriteAssets?.normal;
      const place = scene.positions?.[id] || '';
      const slot = place.includes('ซ้าย') ? 'left' : place.includes('ขวา') || place.includes('ขอบ') ? 'right' : place.includes('กลาง') || place.includes('ล่าง') ? 'center' : place.includes('ฝัน') ? 'left' : actors.length === 1 ? 'center' : index === 0 ? 'left' : 'right';
      const isBackground = /ฉากหลัง|ด้านหลัง|ฝัน/.test(place);
      return path ? `<img class="stage-character slot-${slot} ${isBackground ? 'is-background' : ''} ${speaker === id ? 'is-speaking' : ''}" src="${image(path)}" alt="${esc(character.thaiName)}" />` : '';
    }).join('')}</div>` : ''}
    <div class="scene-credit">${esc(scene.timeOfDay)} <i></i> ${esc(scene.atmosphere)}</div>
  </div>`;
}

function renderChoice(choice) {
  const selected = state.choiceAnswer;
  const alreadyAnswered = Object.hasOwn(state.answered, choice.choiceId);
  const answer = selected || state.answered[choice.choiceId];
  const showFeedback = Boolean(answer);
  const result = answer === choice.correctAnswer;
  return `<section class="choice-sheet" aria-label="คำถามประจำฉาก"><div class="choice-heading"><span>ชวนคิด</span><h2>${esc(choice.question)}</h2></div><div class="choice-options">${choice.options.map((option) => {
    const isCorrect = option.optionId === choice.correctAnswer;
    const isSelected = option.optionId === answer;
    return `<button class="choice-option ${showFeedback && isCorrect ? 'is-correct' : ''} ${showFeedback && isSelected && !isCorrect ? 'is-wrong' : ''}" data-action="answer" data-option="${esc(option.optionId)}" ${showFeedback || alreadyAnswered ? 'disabled' : ''}><span>${esc(option.optionId)}</span>${esc(option.text)}</button>`;
  }).join('')}</div>${showFeedback ? `<p class="choice-feedback ${result ? 'feedback-good' : 'feedback-corrective'}">${esc(result ? choice.feedback.correct : choice.feedback.incorrect)}<br /><small>${esc(choice.feedback.explanation)}</small></p>` : ''}<button class="button button-primary continue-after-choice" data-action="next-scene" ${showFeedback ? '' : 'disabled'}>${state.sceneIndex === scenes.length - 1 ? 'ทำแบบทบทวนต่อ' : 'ไปฉากถัดไป'}</button></section>`;
}

function renderStory() {
  state.screen = 'story';
  persist();
  const scene = currentScene();
  const dialogue = currentDialogue();
  const choice = state.lineIndex >= scene.dialogues.length - 1 ? choices[scene.choiceId] : null;
  const progress = ((scene.sceneOrder - 1 + (state.lineIndex + 1) / scene.dialogues.length) / scenes.length) * 100;
  app.innerHTML = `<section class="story-screen">${renderStage(scene, dialogue)}<div class="story-lower">
    <div class="story-progress"><div class="progress-rail"><span style="width:${progress}%"></span></div><span>เรื่องราว ${sceneNumber(scene)} / 08</span></div>
    ${choice ? renderChoice(choice) : `<button class="dialogue-panel" data-action="advance" aria-label="บทถัดไป"><span class="dialogue-ornament" aria-hidden="true">❧</span><span class="speaker-name">${esc(names[dialogue.speaker] || dialogue.speaker)}</span><span class="dialogue-text">${esc(dialogue.text)}</span><span class="dialogue-hint">แตะเพื่ออ่านต่อ <b>↵</b></span></button>`}
  </div><footer class="story-controls"><button data-action="menu">หน้าแรก</button><div class="scene-dots">${scenes.map((item, index) => `<button class="scene-dot ${index === state.sceneIndex ? 'active' : ''} ${index < state.sceneIndex ? 'visited' : ''}" data-action="go-scene" data-index="${index}" aria-label="ไปฉาก ${index + 1}"></button>`).join('')}</div><button data-action="vocabulary">คำศัพท์</button></footer>${state.drawer === 'vocabulary' ? renderVocabularyDrawer() : ''}</section>`;
}

function persist() {
  localStorage.setItem('plai-ngam-scene', String(state.sceneIndex));
  localStorage.setItem('plai-ngam-line', String(state.lineIndex));
  localStorage.setItem('plai-ngam-screen', state.screen);
  localStorage.setItem('plai-ngam-quiz-index', String(state.quizIndex));
  localStorage.setItem('plai-ngam-score', String(state.score));
  localStorage.setItem('plai-ngam-answered', JSON.stringify(state.answered));
  localStorage.setItem('plai-ngam-quiz-answers', JSON.stringify(state.quizAnswers));
  localStorage.setItem('plai-ngam-quiz-score', String(state.quizScore));
}
function advance() {
  if (state.lineIndex < currentScene().dialogues.length - 1) state.lineIndex += 1;
  persist();
  renderStory();
}
function goNextScene() {
  if (state.sceneIndex < scenes.length - 1) {
    state.sceneIndex += 1; state.lineIndex = 0; state.choiceAnswer = null; state.drawer = null; persist(); renderStory();
  } else {
    state.quizIndex = Number(localStorage.getItem('plai-ngam-quiz-index') || 0);
    renderQuiz();
  }
}

function renderQuiz() {
  state.screen = 'quiz';
  state.quizAnswer = null;
  persist();
  const item = quiz[state.quizIndex];
  if (!item) return renderResults();
  const savedAnswer = state.quizAnswers[item.questionId];
  const answer = savedAnswer || state.quizAnswer;
  const isAnswered = Boolean(answer);
  const isCorrect = answer === item.correctAnswer;
  const progress = (state.quizIndex / quiz.length) * 100;
  app.innerHTML = `<section class="quiz-screen">
    <header class="quiz-topbar"><button class="icon-button" data-action="menu" aria-label="กลับหน้าแรก">⌂</button><span>แบบทบทวนท้ายเรื่อง</span><span>ข้อ ${state.quizIndex + 1} / ${quiz.length}</span></header>
    <div class="quiz-progress"><span style="width:${progress}%"></span></div>
    <main class="quiz-main"><div class="quiz-card"><span class="quiz-category">${esc(item.category === 'story' ? 'ลำดับเรื่อง' : 'ชวนวิเคราะห์')}</span><h1>${esc(item.question)}</h1>
      <div class="quiz-options">${item.options.map((option) => `<button class="quiz-option ${isAnswered && option.optionId === item.correctAnswer ? 'is-correct' : ''} ${isAnswered && option.optionId === answer && !isCorrect ? 'is-wrong' : ''}" data-action="quiz-answer" data-option="${esc(option.optionId)}" ${isAnswered ? 'disabled' : ''}><span>${esc(option.optionId)}</span>${esc(option.text)}</button>`).join('')}</div>
      ${isAnswered ? `<div class="quiz-feedback ${isCorrect ? 'is-correct' : 'is-wrong'}"><strong>${isCorrect ? 'คำตอบถูกต้อง' : 'ลองทบทวนคำอธิบาย'}</strong><p>${esc(item.explanation)}</p></div><button class="button button-primary quiz-next" data-action="quiz-next">${state.quizIndex === quiz.length - 1 ? 'ดูผลการเรียนรู้' : 'ข้อต่อไป'}</button>` : ''}
    </div></main><footer class="quiz-footer"><span>ตอบถูกข้อละ ${quiz[0]?.score ?? 0} คะแนน</span><span>คะแนนเรื่องเล่า ${state.score}</span></footer>
  </section>`;
}

function renderResults() {
  state.screen = 'results';
  const right = quiz.filter((item) => state.quizAnswers[item.questionId] === item.correctAnswer).length;
  const maxScore = choiceData.choices.reduce((sum, item) => sum + item.score, 0) + quizData.totalScore;
  const finalScore = state.score + state.quizScore;
  app.innerHTML = `<section class="ending-screen results-screen" style="--menu-art:url('${image('assets/backgrounds/main_menu/bg_main_menu.webp')}')"><div class="ending-card result-card"><span class="seal-mark">พล</span><small>จบบทเรียน</small><h1>เส้นทางของพลายงาม</h1><p>คุณอ่านเรื่องราวครบทั้ง 8 ฉาก และตอบแบบทบทวนถูก ${right} จาก ${quiz.length} ข้อ</p><div class="score-seal"><strong>${finalScore}</strong><span>/ ${maxScore} คะแนน</span></div><div class="title-actions"><button class="button button-primary" data-action="restart">เริ่มเรื่องอีกครั้ง</button><button class="button button-quiet" data-action="menu">กลับหน้าแรก</button></div></div></section>`;
  for (const key of ['plai-ngam-scene', 'plai-ngam-line', 'plai-ngam-screen', 'plai-ngam-quiz-index']) localStorage.removeItem(key);
  state.sceneIndex = 0;
}

app.addEventListener('click', (event) => {
  const button = event.target.closest('[data-action]');
  if (!button) return;
  const action = button.dataset.action;
  if (action === 'start') {
    state.drawer = null;
    if (localStorage.getItem('plai-ngam-screen') === 'quiz') {
      state.quizIndex = Number(localStorage.getItem('plai-ngam-quiz-index') || 0);
      renderQuiz();
    } else if (localStorage.getItem('plai-ngam-scene') !== null) {
      state.sceneIndex = Number(localStorage.getItem('plai-ngam-scene'));
      state.lineIndex = Number(localStorage.getItem('plai-ngam-line') || 0);
      renderStory();
    } else {
      state.sceneIndex = 0; state.lineIndex = 0; state.score = 0; state.quizScore = 0;
      state.quizAnswers = {}; state.answered = {}; state.quizIndex = 0;
      persist(); renderStory();
    }
  }
  if (action === 'chapters') { state.drawer = 'chapters'; renderMenu(); }
  if (action === 'vocabulary') { state.drawer = 'vocabulary'; state.screen === 'story' ? renderStory() : renderMenu(); }
  if (action === 'close-drawer') { state.drawer = null; state.screen === 'story' ? renderStory() : renderMenu(); }
  if (action === 'menu') { state.drawer = null; renderMenu(); }
  if (action === 'advance') advance();
  if (action === 'next-scene') goNextScene();
  if (action === 'go-scene') { state.sceneIndex = Number(button.dataset.index); state.lineIndex = 0; state.choiceAnswer = null; state.drawer = null; persist(); renderStory(); }
  if (action === 'restart') { state.sceneIndex = 0; state.lineIndex = 0; state.score = 0; state.quizScore = 0; state.quizIndex = 0; state.quizAnswers = {}; state.answered = {}; state.choiceAnswer = null; state.drawer = null; persist(); renderStory(); }
  if (action === 'answer') {
    const choice = choices[currentScene().choiceId];
    if (!choice || Object.hasOwn(state.answered, choice.choiceId)) return;
    state.choiceAnswer = button.dataset.option; state.answered[choice.choiceId] = state.choiceAnswer;
    if (state.choiceAnswer === choice.correctAnswer) state.score += choice.score;
    persist(); renderStory();
  }
  if (action === 'quiz-answer') {
    const item = quiz[state.quizIndex];
    if (!item || state.quizAnswers[item.questionId]) return;
    const answer = button.dataset.option;
    state.quizAnswers[item.questionId] = answer;
    if (answer === item.correctAnswer) state.quizScore += item.score;
    persist(); renderQuiz();
  }
  if (action === 'quiz-next') { state.quizIndex += 1; persist(); renderQuiz(); }
});

app.addEventListener('keydown', (event) => {
  if (state.screen === 'story' && (event.key === 'Enter' || event.key === ' ')) {
    if (event.target === document.body || event.target === app) advance();
  }
});

renderMenu();
