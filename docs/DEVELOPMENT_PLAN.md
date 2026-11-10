# Development Plan — Project Phases

## สถานะ Workspace

ตรวจสอบเมื่อ 9 พฤศจิกายน 2026: Workspace เดิมว่างเปล่า ไม่พบ source code หรือ package configuration จึงเริ่มโครงสร้างใหม่โดยไม่ทับไฟล์เดิม; ต่อมาผู้ใช้เพิ่มชุดภาพไว้ที่ `pics/assets`

## โครงสร้างที่เตรียมไว้

```text
.
├── docs/
├── public/
│   └── assets/
│       ├── backgrounds/
│       ├── characters/
│       └── ui/
├── src/
│   ├── app/
│   ├── components/
│   ├── data/
│   ├── engine/
│   └── styles/
└── README.md
```

## แผนพัฒนา

1. **Phase 1 — ตรวจสอบและวางแผน:** ตรวจ Workspace กำหนดโครงสร้างเริ่มต้น บันทึกความเสี่ยงและข้อที่ต้องยืนยัน
2. **Phase 2 — Storyboard และ Content Database:** ทำ Storyboard 8 ฉากและ Choice Database ให้ตรวจสอบก่อนพัฒนา พร้อมแยกข้อมูลออกจาก engine
3. **Phase 2.5 — Art Assets:** สร้างและตรวจ Character Sheet, Sprite, Background, Event CG และ UI assets; เชื่อม manifest/JSON
4. **Phase 3 — UI/UX:** ออกแบบและพัฒนาหน้า Main Menu และ Story Screen ก่อน ขยายไปหน้าที่เหลือตามลำดับ พร้อม responsive และ accessibility
5. **Phase 4 — Game Engine:** ทำ Scene Manager, Dialogue, Choice/Feedback, Score, Vocabulary, LocalStorage Save/Load, Final Quiz และ Result Screen
6. **Phase 5 — QA:** ตรวจลำดับฉาก การแสดงบทสนทนา คะแนนซ้ำ การบันทึก/โหลด คำศัพท์ การเล่นจบ และ responsive

## ความเสี่ยงและข้อที่ต้องยืนยันก่อน Phase 2

- ยังไม่ระบุฉบับเรียนหรือแหล่งอ้างอิงวรรณคดี จึงยังยืนยันรายละเอียดและลำดับเหตุการณ์ใน Outline ทั้ง 8 ฉากไม่ได้
- บทสนทนาใหม่ต้องระบุชัดว่าเป็นบทเรียบเรียงสำหรับเกม ไม่ใช่คำประพันธ์ต้นฉบับ
- ยังไม่ได้กำหนดเทคโนโลยีเว็บและรูปแบบ asset; ควรเลือกเมื่อเริ่มการออกแบบ UI/UX โดยคำนึงถึงการนำไปเป็นต้นแบบโครงการวิจัย
- ฉากการทำร้ายเด็กควรนำเสนอให้เหมาะกับกลุ่มอายุ 12–15 ปี โดยไม่เพิ่มรายละเอียดรุนแรงเกินจำเป็น

## สถานะ Phase 2

จัดทำ Storyboard, บทสนทนา, Choice Database, คำศัพท์, Final Quiz และข้อมูล JSON แล้ว; ประเด็นแหล่งอ้างอิงยังบันทึกไว้ใน `storyboard.md`.

## สถานะ Phase 2.5

ปิดสำหรับต้นแบบตามการอนุมัติของผู้ใช้ให้ใช้ภาพทั้งชุด: Character Sheet 7, Sprite 30, Background 9, Event CG 4 และ UI SVG 7 รายการ ระบบ manifest เชื่อม asset ครบ; ภาพฉาก 6 และ CG ถูกใช้ตามชุดปัจจุบัน

## สถานะ Phase 3–5

- **Phase 3 — UI/UX:** เสร็จสำหรับต้นแบบ: Main Menu, สารบัญ, Story Screen, ตัวเลือกประจำฉาก, คลังศัพท์, Final Quiz และ Result screen; จัดวาง CG เต็มกรอบและจัดตัวอักษรในกล่องบทสนทนาให้กึ่งกลางแบบ responsive
- **Phase 4 — Game Engine:** เสร็จ: ลำดับ dialogue/scene, choice feedback, scoring, บันทึกและ resume ใน localStorage, final quiz, result และ restart
- **Phase 5 — QA:** ผ่านการตรวจ asset/JSON, JavaScript syntax, browser flow ตั้งแต่บทสนทนาถึงผลลัพธ์ และ preview ที่ mobile/desktop

โครงการพร้อม deploy เป็น static site; สร้างไฟล์ปล่อยด้วย `python scripts/deploy/build_static.py` แล้วอ่าน `DEPLOY.md` และ `QA_REPORT.md`.

## ขอบเขต Phase 1

สร้างเฉพาะโครงสร้างไดเรกทอรีและเอกสารเริ่มต้น ยังไม่ได้สร้างเนื้อเรื่อง UI, source code, ระบบเกม หรือภาพประกอบ
