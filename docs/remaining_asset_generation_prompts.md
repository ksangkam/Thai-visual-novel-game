# Prompt Pack — Remaining Phase 2.5 Art

ใช้กับ ChatGPT Images หรือ image generator ที่รับภาพอ้างอิงได้ สร้างทีละภาพตามรหัสไฟล์ด้านล่าง แล้วส่งไฟล์ต้นฉบับกลับมาโดยคงชื่อไฟล์ไว้

## ลำดับทำงาน

1. สร้าง Character Design Sheet ทั้ง 7 ภาพก่อน ใช้ภาพ `cg_scene05.webp` เป็น reference สไตล์โดยเฉพาะงานเส้นและใบหน้าของวันทอง/พลายงาม (อย่าลอกองค์ประกอบฉาก)
2. สร้าง Sprite ทีละอารมณ์ โดยแนบ Sheet ของตัวละครคนนั้นทุกครั้ง ใช้ prompt sprite กลางด้านล่างและแทน `[CHARACTER]`, `[EXPRESSION]`, `[PALETTE]` ตามตาราง
3. สร้าง Background ทีละฉาก โดยแนบ `bg_scene01.webp` และ `bg_scene02.webp` เป็น style references
4. สร้าง Event CG ที่เหลือ โดยแนบ `cg_scene05.webp` เป็น style reference

ภาพ style reference ที่อยู่ในโปรเจกต์:

- `public/assets/backgrounds/scenes/bg_scene01.webp`
- `public/assets/backgrounds/scenes/bg_scene02.webp`
- `public/assets/backgrounds/cg/cg_scene05.webp`

Prompt ด้านล่างเป็นภาษาอังกฤษเพื่อช่วยให้โมเดลทำตามข้อกำหนดภาพได้สม่ำเสมอ แต่ชื่อไทยและบทบาทตัวละครกำกับไว้ด้วย

## Master art direction

ใส่ข้อความนี้ต่อท้าย Prompt ของทุกภาพ:

```text
Art direction: premium 2D Thai historical visual novel illustration, elegant anime-inspired character design with polished clean line art and natural anatomy; painterly, richly detailed environments; soft cinematic lighting; expressive but restrained acting; historically inspired central Thai setting, not a claim of exact documentary reconstruction. Unified palette: burgundy #6D3036, gold #C6A15B, teak #3C3028, ivory #F3E9D2, and forest green #526C56, adjusted naturally for time of day. No chibi, no pixel art, no 3D render, no photorealism, no Japanese or Chinese architecture/costume cues, no modern objects, no text, no logo, no watermark.
```

## 1. Character design sheets — 7 images

Each prompt creates one clean 4:5 portrait character reference sheet on a plain warm ivory background. Show the *same person* in all views: full-body front, full-body three-quarter, face close-up, costume-detail inset(s), and small color swatches. Keep all views large enough to inspect. Do not print labels or lettering.

### `public/assets/characters/phlai_ngam/design_sheet.png`

```text
Create one professional 4:5 portrait character design sheet for Phlai Ngam (พลายงาม), the Thai-literature protagonist, a Thai boy about 9 years old. Age-appropriate child proportions, gentle distinctive face, observant dark eyes, black hair, simple historically inspired child's clothing in indigo, ivory, and light brown. He should read as innocent, brave, and determined without looking like an adult or a small child. Show full-body front and three-quarter views, a large face close-up, costume/fabric details, and color swatches. Repeat the identical face, hair, skin tone, body proportions, clothing, and accessories in every view. Plain warm ivory studio sheet, no environment, no extra people, no weapons, no text or labels. [Append the Master art direction.]
```

### `public/assets/characters/wantong/design_sheet.png`

```text
Create one professional 4:5 portrait character design sheet for Wantong (วันทอง), Phlai Ngam's adult Thai mother. Dignified, beautiful but natural Thai face; long dark hair in a historically inspired Thai style; graceful adult proportions; modest traditional sabai and chong kraben, muted burgundy, warm ivory, and restrained gold. Her character should feel gentle, loving, protective, and quietly strong. Show full-body front and three-quarter views, a large face close-up, costume/fabric details, and color swatches. Repeat the identical identity and costume in all views. Plain warm ivory studio sheet, no environment, no extra people, no text or labels. Use the attached cg_scene05 only as a broad style and face-design reference, not as a composition to copy. [Append the Master art direction.]
```

### `public/assets/characters/khunchang/design_sheet.png`

```text
Create one professional 4:5 portrait character design sheet for Khun Chang (ขุนช้าง), the wealthy adult Thai antagonist. He is distinctly bald with a heavyset build and a broad, expressive face; make him visually different from the handsome, athletic Khun Phaen. Historically inspired high-status Thai clothing and restrained jewelry, deep plum, brick red, teak, and muted gold. His design should support displeasure, anger, suspicion, and a sly smirk without becoming grotesque or comedic. Show full-body front and three-quarter views, face close-up, clothing/jewelry details, and color swatches. Maintain the exact same identity and costume across views. Plain warm ivory studio sheet, no environment, no extra people, no text or labels. [Append the Master art direction.]
```

### `public/assets/characters/khunphaen/design_sheet.png`

```text
Create one professional 4:5 portrait character design sheet for Khun Phaen (ขุนแผน), Phlai Ngam's adult Thai father. A tall, graceful, confident and courageous Thai man with a composed handsome face and dark hair tied neatly back; athletic, mature proportions. Historically inspired noble/warrior clothing, elegant rather than excessively armored, deep green, teak, ivory, and gold. Make his silhouette and personality unmistakably different from the bald, heavyset Khun Chang. Show full-body front and three-quarter views, face close-up, costume details, and color swatches. Keep the same identity and costume in every view. Plain warm ivory studio sheet, no environment, no extra people, no text or labels. [Append the Master art direction.]
```

### `public/assets/characters/thongprasi/design_sheet.png`

```text
Create one professional 4:5 portrait character design sheet for Thong Prasi (ทองประศรี), Phlai Ngam's elderly Thai grandmother. Make her unmistakably elderly, with kind mature facial features, gentle age lines, a calm dignified posture, and simple modest historically inspired Thai women's clothing. Muted brown, teak, ivory, and aged gold. Warm, respected, resilient presence; not a young woman. Show full-body front and three-quarter views, face close-up, clothing/fabric details, and color swatches. Keep the same visibly elderly identity and costume across views. Plain warm ivory studio sheet, no environment, no extra people, no text or labels. [Append the Master art direction.]
```

### `public/assets/characters/khrua_nak/design_sheet.png`

```text
Create one professional 4:5 portrait character design sheet for Khrua Nak (ขรัวนาก), an elderly Thai Buddhist abbot. Shaven head, serene compassionate mature face, modest historically inspired saffron/brown monk's robe worn respectfully and correctly; no jewelry, weapons, fantasy ornaments, or inappropriate accessories. Quiet, wise, and kind presence. Show full-body front and three-quarter views, face close-up, robe-fold details, and restrained color swatches. Maintain identical face, build, robe, and proportions in all views. Plain warm ivory studio sheet, no environment, no other people, no text or labels. [Append the Master art direction.]
```

### `public/assets/characters/hongphrai/design_sheet.png`

```text
Create one professional 4:5 portrait character design sheet for Hong Phrai (โหงพราย), a humanoid supernatural retainer from Thai literary folklore. A clear human-like silhouette with a mysterious but gentle expression, semi-translucent pale blue-gray and silver appearance, subtle controlled glow and mist-like edges. Keep the design suitable for a secondary-school audience: mysterious, not frightening, not bloody, not monstrous. Show full-body front and three-quarter views, face close-up, spectral-clothing/detail studies, and restrained color swatches. Keep all views recognizably the same spirit. Plain warm ivory/very pale gray studio sheet for legibility, no scene, no extra people, no text or labels. [Append the Master art direction.]
```

## 2. Transparent character sprites — 30 images

Generate **one image per expression**, not a multi-character sheet. Attach that character's approved design sheet as the identity reference. Request a true transparent background and save as PNG with alpha. Keep the same waist-up framing, eye line, scale, costume, lighting, and horizontal position for every expression of the same character. Leave clear space around hair, shoulders, and hands. Hands may be omitted below the chest if they are not needed. No cast shadow, props, background, text, or frame.

### Sprite prompt template

```text
Using the attached approved character design sheet as the exact identity reference, create one production-ready visual-novel character sprite of [CHARACTER] showing the [EXPRESSION] expression. Preserve the character's face shape, eye shape, hair, age, skin tone, body proportions, clothing, accessories, and palette exactly. Waist-up, centered at the same scale and eye-line as the other sprites in this character set, natural anatomy and clean polished line art, readable restrained facial acting. Actual transparent background with a clean alpha edge; no checkerboard, no backdrop, no cast shadow, no prop, no text, no border, no watermark. Portrait PNG, full head and shoulders visible with generous transparent padding. [Append the Master art direction.]
```

| Character | Palette | Generate one file for each expression |
|---|---|---|
| `phlai_ngam` / พลายงาม, 9-year-old boy | indigo, ivory, light brown | `normal`, `happy`, `sad`, `surprised`, `worried` |
| `wantong` / วันทอง, adult mother | muted burgundy, ivory, soft gold | `normal`, `happy`, `sad`, `worried`, `crying` |
| `khunchang` / ขุนช้าง, bald heavyset wealthy man | deep plum, brick red, muted gold | `normal`, `angry`, `suspicious`, `surprised`, `smirk` |
| `khunphaen` / ขุนแผน, confident adult noble/warrior | deep green, teak, gold | `normal`, `confident`, `serious`, `angry`, `surprised` |
| `thongprasi` / ทองประศรี, elderly grandmother | brown, teak, aged gold | `normal`, `happy`, `surprised`, `sad` |
| `khrua_nak` / ขรัวนาก, elderly monk | saffron, muted brown | `normal`, `happy`, `serious` |
| `hongphrai` / โหงพราย, gentle humanoid spirit | pale blue-gray, silver | `normal`, `mysterious`, `alert` |

Filename pattern: `[character_id]_[expression].png`, for example `phlai_ngam_worried.png` in the project folder `public/assets/characters/phlai_ngam/`.

Use these expression cues in place of `[EXPRESSION]` in the sprite template:

| Expression code | Acting direction |
|---|---|
| `normal` | calm attentive neutral face, relaxed brows and mouth |
| `happy` | warm gentle smile, bright relaxed eyes |
| `sad` | downcast eyes, slightly raised inner brows, restrained sadness |
| `surprised` | widened eyes, raised brows, slightly parted lips |
| `worried` | brows drawn together, tense attentive eyes, small uncertain mouth |
| `crying` | visible tears and grief, keep facial anatomy natural and dignified |
| `angry` | firm lowered brows, focused eyes, controlled tense mouth |
| `suspicious` | narrowed assessing eyes, one brow subtly raised |
| `smirk` | small asymmetrical sly smile, calculating eyes, not comedic |
| `confident` | steady direct gaze, composed half-smile, upright bearing |
| `serious` | focused calm eyes, neutral firm mouth |
| `mysterious` | quiet unreadable gaze, subtle spectral glow, gentle not frightening |
| `alert` | attentive widened eyes, poised but not aggressive |

**Database note:** The Phase 2.5 expression table above totals 30 sprites. `data/characters.json` currently has a few different expression names (for example, it requests `angry` for Phlai Ngam while the Phase 2.5 table does not). Generate these 30 first; when integrating the returned files, reconcile any database-only expressions instead of assigning a mismatched sprite.

## 3. Missing backgrounds — 6 images

For every background attach `bg_scene01.webp` and `bg_scene02.webp` as style references. Use a wide 16:9 landscape image at the highest available resolution (target at least 1920 × 1080). These are environment plates, not event art: no people or recognizable character silhouettes. Keep the lower third relatively quiet for the dialogue box and preserve lateral staging space for sprites.

### `public/assets/backgrounds/scenes/bg_scene03.webp` — twilight forest path

```text
Wide 16:9 environment plate for a Thai historical visual novel: a winding path through dense old-growth central Thai forest at dusk, enormous rain trees, layered tropical foliage, patches of fading amber light filtering through the canopy, deepening shadows and a quiet uneasy mood. Keep the path readable through the center, sides available for character sprites, and the lower third dark/simple enough for dialogue UI. No people, no figures, no blood, no injury, no weapons, no text, no modern objects. [Append the Master art direction.]
```

### `public/assets/backgrounds/scenes/bg_scene04.webp` — moonlit rescue forest

```text
Wide 16:9 environment plate: the same kind of Thai forest clearing at night, an old fallen log beside a safe open patch of ground, cool moonlight through the trees, thin silver-blue mist and only a faint restrained supernatural glow in the distance. Mysterious but reassuring, as if danger has passed. Leave space at center and sides for sprites and keep the lower third unobtrusive for dialogue UI. No people, no spirit figure, no blood, no injury detail, no text, no modern objects. [Append the Master art direction.]
```

### `public/assets/backgrounds/scenes/bg_scene05.webp` — near-dawn meeting place

```text
Wide 16:9 environment plate for the reunion scene: a quiet Thai forest clearing near dawn, soft peach-gold light entering through trees, a sheltered patch of ground and a few distant forest details suggesting the place where a mother has found her son. Calm, tender, and safe after a frightening night. Leave two clear staging areas left and right for sprites and keep the lower third quiet for dialogue UI. No people, no text, no logo, no modern objects. [Append the Master art direction.]
```

### `public/assets/backgrounds/scenes/bg_scene06.webp` — temple pavilion at night to dawn

```text
Wide 16:9 environment plate: a modest old Thai temple pavilion and wooden sala, historically inspired central Thai architecture, simple wooden pillars and a quiet sheltered area, transitioning from deep blue night toward the first pale dawn light. The mood is solemn, peaceful, and bittersweet, with a clear center for three character sprites and a dark/simple lower third for dialogue UI. Respectful Buddhist setting; no people, no statues as focal subjects, no text, no modern objects. [Append the Master art direction.]
```

### `public/assets/backgrounds/scenes/bg_scene07.webp` — route to Kanchanaburi

```text
Wide 16:9 environment plate: an old rural path leading toward distant Kanchanaburi, broad rice fields, tropical tree line, gentle hills and forest on the horizon, early morning sunlight. Convey a lonely but hopeful journey; the path should lead the viewer's eye into the distance. Keep the lower third and one side uncluttered for visual-novel UI and a walking sprite. No people, carts, roads, power lines, text, or modern objects. [Append the Master art direction.]
```

### `public/assets/backgrounds/scenes/bg_scene08.webp` — grandmother's house

```text
Wide 16:9 environment plate: a welcoming traditional Thai teak house in the Kanchanaburi countryside, front porch and shaded yard clearly visible, warm afternoon light, a safe domestic atmosphere that feels like the beginning of a new life. Compose an open porch area for an elderly woman sprite and a lower foreground area for a child sprite; keep the lower third unobtrusive for dialogue UI. No people, no text, no logo, no modern objects. [Append the Master art direction.]
```

## 4. Missing event CG — 3 images

Attach `cg_scene05.webp` as an illustration-style reference. Unlike backgrounds, these images include characters and tell a specific story beat. Use wide 16:9 framing; no text.

### `public/assets/backgrounds/cg/cg_scene01.webp` — Phlai Ngam's birth

```text
Create a polished 16:9 narrative event illustration for a Thai historical visual novel: inside a warm traditional Thai teak room, adult mother Wantong gently cradles her newborn son Phlai Ngam after a safe birth. Focus on tenderness, relief, and the first family moment; tasteful and fully non-graphic, no medical details. Warm natural window light, elegant historically inspired Thai clothing and room decor, careful cinematic staging. Keep faces and the baby unobscured. No text, no logo, no watermark, no modern objects. [Append the Master art direction.]
```

### `public/assets/backgrounds/cg/cg_scene03.webp` — danger in the forest, non-graphic

```text
Create a carefully staged 16:9 event illustration for a secondary-school Thai historical visual novel, depicting the aftermath of a forest ambush without showing violence: young Phlai Ngam lies safely unconscious on a patch of ground beside a fallen log, fully clothed and with no visible wound or blood; Khun Chang is only a distant shadow leaving along the winding forest path. Use distance, framing, and dusk shadows to imply the danger, never a blow or injury. Serious, restrained, non-horror, non-graphic. No weapons, no gore, no text, no watermark, no modern objects. [Append the Master art direction.]
```

### `public/assets/backgrounds/cg/cg_scene08.webp` — meeting Thong Prasi

```text
Create a polished 16:9 narrative event illustration: at the porch of a traditional Thai teak house in Kanchanaburi, young Phlai Ngam respectfully performs a wai before his elderly grandmother Thong Prasi. She looks surprised and warmly moved, beginning to welcome him inside. Warm afternoon sunlight, safe family atmosphere, clear readable gestures, respectful period clothing and architecture. Keep both characters' faces, hands, and silhouettes clear. No text, no logo, no watermark, no modern objects. [Append the Master art direction.]
```

## After generation

- Keep the original downloaded files; do not overwrite the existing project images.
- Use PNG for character sheets and transparent sprites; check that sprite PNGs truly have alpha transparency.
- Use PNG or WebP for backgrounds and event CG; preserve 16:9.
- Send images with their matching filenames or include the filename in your message. Generate in batches if convenient; the names above identify each image.
- If the model can't create true transparent PNGs, send the sprite anyway and tell me which tool/output format you used. I will check whether it can be cleanly processed before registering it.
