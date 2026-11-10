# Phase 2.5 — Asset Integration

## สถานะ

**ปิดสำหรับต้นแบบตามการอนุมัติของผู้ใช้** ให้ใช้ภาพใน `pics/assets` ทั้งชุด แม้การตรวจภาพก่อนหน้าจะทำเครื่องหมายภาพพื้นหลัง `bg_scene06` และความต่อเนื่องของเครื่องแต่งกายใน Event CG ทั้งสี่ไว้ให้พิจารณา ผู้ใช้ยืนยันให้ใช้ภาพเหล่านี้และดำเนิน Phase 3 ต่อ

## Inventory และ integration

| กลุ่ม | จำนวน | ปลายทาง |
|---|---:|---|
| Character Sheet | 7 | `public/assets/characters/[id]/design_sheet.png` |
| Expression Sprite | 30 | `public/assets/characters/[id]/*_*.png` |
| Background (เมนู + 8 ฉาก) | 9 | `public/assets/backgrounds/` |
| Event CG | 4 | `public/assets/backgrounds/cg/` |
| UI SVG | 7 | `public/assets/ui/` |

ไฟล์ต้นฉบับคงอยู่ใน `pics/assets`; ไฟล์ raster ที่ใช้ในเกมเป็นไฟล์ที่แปลง/ปรับขนาดเพื่อการแสดงผล ส่วน `data/scenes.json`, `data/characters.json` และ `public/assets/manifest/asset_manifest.json` เชื่อมไปยัง asset ที่ใช้งานครบแล้ว

## ตรวจสอบไฟล์

สคริปต์ `scripts/asset_processing/validate_integrated_assets.py` ตรวจไฟล์ภาพ raster, มิติ/รูปแบบ, alpha ของ sprite, SVG และ path อ้างอิง JSON ได้ผ่าน ไม่มีไฟล์เสียหรือ path ขาดหาย

## หมายเหตุจากการตรวจภาพ

ภาพ `bg_scene06` มีบุคคลอยู่ในภาพพื้นหลัง และ CG `cg_scene01`, `cg_scene03`, `cg_scene05`, `cg_scene08` มีความต่างด้านเครื่องแต่งกายเมื่อเทียบกับ Character Sheet ข้อสังเกตนี้ถูกบันทึกไว้เพื่อให้ทีมพิจารณาก่อนเผยแพร่ผลงานจริง แต่ไม่ได้ขวางการทำต้นแบบ Phase 3 ตามคำสั่งผู้ใช้
