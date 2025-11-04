# Generator Sertifikat Otomatis

Generator sertifikat pelatihan berbasis **FastAPI + React** yang dapat menghasilkan sertifikat secara massal dari file Excel/CSV dengan hasil format PNG dan PDF.

## ✨ Fitur

- 🎨 **Upload Template**: Upload template sertifikat kustom dalam format PNG
- 📊 **Import Data**: Support file Excel (.xlsx, .xls) dan CSV
- 🖼️ **Generate Otomatis**: Buat sertifikat PNG + PDF untuk setiap peserta
- 📦 **Download ZIP**: Semua sertifikat langsung dikompress dalam satu file ZIP
- 🔄 **Auto-Scaling**: Layout otomatis menyesuaikan ukuran template
- 🌏 **Bilingual**: Teks Indonesia dan English
- 📱 **Responsive UI**: Tampilan modern dan mobile-friendly
- 💾 **History MongoDB**: Simpan riwayat generate di database
- 🔍 **QR Code**: Setiap sertifikat dilengkapi QR code unik

## 📋 Format File Excel/CSV

File data peserta harus memiliki 3 kolom wajib:

| Kolom | Deskripsi | Format |
|-------|-----------|--------|
| `name` | Nama peserta | Text |
| `course` | Nama pelatihan | Text |
| `date` | Tanggal pelatihan | YYYY-MM-DD atau DD/MM/YYYY |

### Contoh Excel:

| name | course | date |
|------|--------|------|
| Fani Resita Ningsih | Pelatihan Pembuatan Wrap | 2025-08-05 |
| Budi Santoso | Food Safety Training | 2025-09-15 |
| Siti Nurhaliza | Customer Service Excellence | 2025-10-20 |

## 🎯 Cara Penggunaan

### 1. Upload Template
- Klik area "Klik untuk pilih template"
- Pilih file PNG sertifikat (landscape, disarankan 3000×2000 px)
- Template akan otomatis terupload

### 2. Upload Data Peserta
- Klik area "Klik untuk pilih file Excel/CSV"
- Pilih file Excel atau CSV dengan kolom `name`, `course`, `date`

### 3. Generate Sertifikat
- Klik tombol "Generate Sertifikat"
- Tunggu proses generate selesai
- File ZIP akan otomatis terdownload

## 📝 Detail Layout Sertifikat

Setiap sertifikat otomatis mencakup:

- ✅ Judul "Training Certificate" (green, italic, center)
- ✅ Deskripsi bilingual (ID/EN)
- ✅ Nama peserta (bold, underline, center)
- ✅ "Telah mengikuti / Has attended"
- ✅ Nama pelatihan + subjudul English
- ✅ Paragraf penyelenggara (PT Aerofood Indonesia)
- ✅ Tanggal Indonesia + English
- ✅ QR Code berisi: nama | course | tanggal
- ✅ Tanda tangan "Rakhmat Syarifudin"
- ✅ Jabatan "VP Human Capital Management"

**Semua teks center-aligned dan auto-scaled**

## 🛠️ Tech Stack

- **Backend**: FastAPI, Pillow, pandas, qrcode, reportlab
- **Frontend**: React, Tailwind CSS, Shadcn/UI
- **Database**: MongoDB
