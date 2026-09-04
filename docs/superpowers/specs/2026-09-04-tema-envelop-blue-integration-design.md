# Desain Integrasi Tema Envelope Blue (TemaEnvelopBlue)

## 1. Ikhtisar (Overview)
Dokumen ini merinci arsitektur dan spesifikasi teknis untuk mengintegrasikan tema **Envelope Blue** (`envelope-blue`) ke dalam ekosistem **Qinvi**:
1. **Backend (`qinvi`)**: Registrasi konfigurasi tema `TemaEnvelopBlue`, data seeder demo, dan SSR redirection.
2. **Admin Dashboard (`admin-dashboard`)**: Menampilkan tema di daftar tema dan menyediakan kontrol kustomisasi pada `TabThemeOverride` (warna biru, foto cover & prewedding, kutipan ayat/Arab, dan dresscode).
3. **Frontend (`envelope-blue`)**: Menghubungkan template SPA ke backend Qinvi melalui API dynamic data binding, query slug resolution, serta pengiriman RSVP dan ucapan secara live.

---

## 2. Arsitektur & Spesifikasi Komponen

### A. Backend (`qinvi`)
* **Theme Configuration (`src/config/themes/tema-envelop-blue.config.ts`)**:
  * `code`: `'TemaEnvelopBlue'`
  * `name`: `'Tema Envelop Blue'`
  * `category`: `'envelope'`
  * `version`: `1`
  * `is_premium`: `false`
  * `is_active`: `true`
  * `theme_config.colors`:
    * `primary`: `'#3d78a2'` (Deep Ink Blue)
    * `secondary`: `'#65839d'` (Ink Blue)
    * `accent`: `'#9bccdb'` (Soft Sky Blue)
    * `bg_body`: `'#e9faff'` (Pale Water Blue)
    * `paper`: `'#e9faff'`
    * `sheet`: `'#e7f9fe'`
  * `theme_config.fonts`:
    * `script`: `"'Roben Elegante', cursive"`
    * `display`: `"'Roben Elegante', cursive"`
    * `serif`: `"'Cormorant Infant', serif"`
    * `sans`: `"'Jost', system-ui, sans-serif"`
    * `caps`: `"'Activists', serif"`
    * `arabic`: `"'Amiri', serif"`
    * `call`: `"'Cavilenny', cursive"`
    * `verse`: `"'Cinzel', serif"`
* **Database Seeding**:
  * Daftarkan `temaEnvelopBlueConfig` di `src/db/seed-themes.ts`.
  * Buat `src/db/seed-wedding-envelop-blue.ts`:
    * Slug: `tema-envelop-blue`
    * Title: `Ahmad & Salma`
    * Theme code: `TemaEnvelopBlue`
    * Menyiapkan data mempelai, acara (Akad & Resepsi), quote (teks, verse, arabic), dan dresscode (swatches & note).
* **SSR Routing (`src/modules/ssr/ssr.controller.ts`)**:
  * Tambahkan mapping `themeCode === 'TemaEnvelopBlue'` ke `http://localhost:5179` untuk pengalihan instan saat mode pengembangan lokal.

---

### B. Admin Dashboard (`admin-dashboard`)
* **Theme Management (`src/views/ThemeManagement.tsx`)**:
  * Memastikan `TemaEnvelopBlue` dapat dipilih oleh admin dan tergolong dalam kategori `envelope`.
* **Kustomisasi Tema (`src/tabs/TabThemeOverride.tsx`)**:
  * **Color Palette Override**: Menyajikan form warna default token Blue (`#3d78a2`, `#65839d`, `#9bccdb`, `#e9faff`).
  * **Cover & Prewedding Image Controls**: Mengaktifkan slider Zoom & Posisi Foto (`spousePhotoTransform`) saat tema yang aktif adalah `TemaEnvelopBlue`.
  * **Quote & Arabic Ayat Editor**:
    * Input Teks Kutipan Terjemahan (`quote.text`).
    * Input Nama Surat / Sumber Kutipan (`quote.verse`).
    * Input Teks Arab (`quote.arabic`) yang disimpan ke `theme_override.quote.arabic`.
  * **Dresscode Customization**:
    * Input panduan berpakaian (`theme_override.dresscode.note`).
    * 4 color picker untuk lingkaran warna dresscode (`theme_override.dresscode.colors`).

---

### C. Frontend (`envelope-blue`)
* **API Client & Slug Resolution (`src/lib/api.ts`)**:
  * Menggunakan `DEFAULT_SLUG = 'tema-envelop-blue'`.
  * Menangani query param `?slug=...` serta pengabaian prefix path `/TemaEnvelopBlue` atau `/tema-envelop-blue`.
  * Mengaktifkan request live API saat `VITE_LIVE_DATA=1` (atau `VITE_DESIGN_MODE=0`).
* **Composable Data (`src/composables/useWedding.ts`)**:
  * Mengaplikasikan warna override ke variabel CSS token tema.
  * Mengekspos data `dresscode`, `quoteArabic`, `quoteText`, `quoteVerse`, `pengantin`, `acara`, `gallery`, `gift`, dan `wishes`.
* **Binding Komponen**:
  * `DresscodeSection.vue`: Render dinamis catatan dresscode dan 4 warna swatch.
  * `BismillahSection.vue` & `QuoteSection.vue`: Render dinamis teks Arab, kutipan, dan surat.
  * `AkadSection.vue` & `ResepsiSection.vue`: Render dinamis tanggal, jam, tempat, dan link peta dari data acara.
  * `GiftSection.vue`: Render nomor rekening / e-wallet.
  * `RsvpSection.vue` & `WishesSection.vue`: Live POST ke endpoint backend `/v1/service/menu/hadir2` dan `/v1/service/menu/ucapan`.

---

## 3. Rencana Verifikasi (Verification Plan)
1. **Backend Verification**: Menjalankan seeder tema dan seeder wedding `tema-envelop-blue`, memverifikasi data di database.
2. **Admin Dashboard Verification**: Membuka dashboard, mengubah warna, kutipan ayat Arab, dan dresscode untuk undangan bertema `TemaEnvelopBlue`, lalu simpan.
3. **Frontend Verification**: Membuka `http://localhost:5179/tema-envelop-blue` (atau `?slug=tema-envelop-blue`), memverifikasi seluruh komponen terisi data nyata dari backend, dan mencoba submit RSVP serta ucapan.
