# 📖 Tutorial Generator Sertifikat Otomatis

Tutorial lengkap cara menggunakan aplikasi Generator Sertifikat Otomatis.

---

## 🌐 Akses Aplikasi

Buka browser dan kunjungi:
```
https://cert-generator-10.preview.emergentagent.com
```

---

## 📥 STEP 1: Download Contoh Excel

### Cara Download Sample File:

1. **Scroll** ke bagian **"Panduan Penggunaan"** (panel kanan)
2. Di bagian **"2. Format File Excel/CSV"**, klik button:
   
   **🔽 Download Contoh Excel**

3. File `sample_participants.xlsx` akan terdownload otomatis

### Isi File Contoh:

| name | course | date |
|------|--------|------|
| Fani Resita Ningsih | Pelatihan Pembuatan Wrap | 2025-08-05 |
| Budi Santoso | Food Safety Training | 2025-09-15 |
| Siti Nurhaliza | Customer Service Excellence | 2025-10-20 |
| Ahmad Hidayat | Leadership Development | 2025-11-10 |
| Dewi Lestari | Digital Marketing Workshop | 2025-12-05 |

---

## ✏️ STEP 2: Edit Data Peserta

1. **Buka file Excel** yang sudah didownload
2. **Edit data** sesuai kebutuhan Anda:
   - Kolom **`name`** → Nama peserta
   - Kolom **`course`** → Nama pelatihan
   - Kolom **`date`** → Tanggal (YYYY-MM-DD)

### Format Tanggal yang Didukung:
- ✅ `2025-08-05` (YYYY-MM-DD) - **Recommended**
- ✅ `05/08/2025` (DD/MM/YYYY)
- ✅ `08/05/2025` (MM/DD/YYYY)

### Contoh Edit:
```
name,course,date
John Doe,Excel Training,2025-11-15
Jane Smith,Leadership Program,2025-12-20
Bob Wilson,Safety Workshop,2025-10-30
```

3. **Simpan file** Excel Anda

---

## 📤 STEP 3: Upload Template Sertifikat

### Cara Upload Template:

1. Di halaman utama, bagian **"1. Upload Template Sertifikat (PNG)"**
2. **Klik area** dengan tulisan **"Klik untuk pilih template"**
3. **Pilih file PNG** template sertifikat Anda
4. Tunggu hingga muncul **✓ "Template berhasil diupload"**

### Catatan Template:
- Format: **PNG, JPG, atau JPEG**
- Ukuran rekomendasi: **3000×2000 px** (landscape)
- Sistem akan **auto-scaling** untuk ukuran lain
- Template harus kosong/polos (teks akan ditambahkan otomatis)

---

## 📊 STEP 4: Upload Data Peserta

### Cara Upload Excel/CSV:

1. Bagian **"2. Upload Data Peserta (Excel/CSV)"**
2. **Klik area** dengan tulisan **"Klik untuk pilih file Excel/CSV"**
3. **Pilih file** Excel (.xlsx, .xls) atau CSV yang sudah diedit
4. Nama file akan muncul di area upload

### Validasi:
✅ File harus memiliki 3 kolom: `name`, `course`, `date`
❌ Jika kolom tidak lengkap, akan muncul error

---

## 🚀 STEP 5: Generate Sertifikat

### Cara Generate:

1. Pastikan template dan data sudah terupload
2. **Klik button hijau besar:**
   
   **⬇️ Generate Sertifikat**

3. **Tunggu proses generate** (loading spinner muncul)
4. File **ZIP otomatis terdownload** setelah selesai

### Proses Generate:
- ⏱️ Waktu: ~2-5 detik per sertifikat
- 📦 Output: 1 file ZIP berisi semua sertifikat
- 💾 Auto-save history ke database

---

## 📦 STEP 6: Extract & Lihat Hasil

### Isi File ZIP:

```
certificates_xxxxx.zip
└── certificates/
    ├── Fani_Resita_Ningsih.png
    ├── Fani_Resita_Ningsih.pdf
    ├── Budi_Santoso.png
    ├── Budi_Santoso.pdf
    └── ...
```

### Cara Extract:

**Windows:**
1. Klik kanan file ZIP
2. Pilih **"Extract All..."**
3. Pilih folder tujuan
4. Klik **"Extract"**

**Mac:**
1. Double-click file ZIP
2. Folder otomatis ter-extract

**Linux:**
```bash
unzip certificates_xxxxx.zip
```

### Lihat Hasil:
- Buka folder `certificates/`
- ✅ File **PNG** → untuk print/digital
- ✅ File **PDF** → untuk email/sharing

---

## 📋 STEP 7: Lihat Riwayat Generate

### Bagian "Riwayat Generate":

Di bagian bawah halaman, Anda akan melihat **history** semua sertifikat yang pernah digenerate:

- 📄 **Nama file** yang diupload
- 👥 **Jumlah peserta**
- 📅 **Tanggal generate**
- ✅ **Status** (completed)

Contoh:
```
✓ sample_participants.xlsx
  3 peserta • 30/10/2025
  Status: completed
```

---

## 🎨 Detail Sertifikat yang Dihasilkan

Setiap sertifikat otomatis berisi:

### Elemen Visual:
1. ✅ **Logo** (dari template Anda)
2. ✅ **Judul** "Training Certificate" (hijau, italic, center)
3. ✅ **Deskripsi bilingual** (ID + EN)
4. ✅ **Nama peserta** (bold, underline, ukuran besar)
5. ✅ **"Telah mengikuti / Has attended"**
6. ✅ **Nama pelatihan** + subjudul English
7. ✅ **Paragraf penyelenggara** (bilingual)
8. ✅ **Tanggal** (format Indonesia + English)
9. ✅ **QR Code** (center-bottom)
10. ✅ **Tanda tangan** "Rakhmat Syarifudin" (underline)
11. ✅ **Jabatan** "VP Human Capital Management"

### Format Tanggal Otomatis:
- **Indonesia**: `5 Agustus 2025`
- **English**: `August 5, 2025`

### QR Code Berisi:
```
Nama Peserta | Nama Course | Tanggal Indonesia
```
Contoh: `Fani Resita Ningsih | Pelatihan Pembuatan Wrap | 5 Agustus 2025`

---

## 💡 Tips & Trik

### ✅ Best Practices:

1. **Template**:
   - Gunakan background dengan warna solid atau gradient lembut
   - Hindari terlalu banyak elemen visual (biar ruang teks cukup)
   - Pastikan contrast warna bagus untuk teks hitam

2. **Data Excel**:
   - Cek ejaan nama dan pelatihan sebelum generate
   - Gunakan tanggal format YYYY-MM-DD untuk konsistensi
   - Hapus baris kosong di Excel

3. **Naming**:
   - Nama file output otomatis dari kolom `name`
   - Spasi akan diganti underscore: `John Doe` → `John_Doe.png`

4. **Ukuran File**:
   - PNG: ~500-600 KB per file
   - PDF: ~750-800 KB per file
   - 100 peserta ≈ 120-130 MB ZIP

### ⚠️ Troubleshooting:

**Error: "Template not found"**
→ Upload template dulu sebelum generate

**Error: "Excel must have columns: name, course, date"**
→ Pastikan nama kolom **exact match** (lowercase)

**Tanggal tidak terformat dengan benar**
→ Gunakan format YYYY-MM-DD (contoh: 2025-08-05)

**File ZIP tidak muncul**
→ Cek browser download folder / allow pop-up

---

## 🔗 Link Penting

### Download Sample:
- **Contoh Excel**: [Download via app button]
- **Sample Sertifikat PNG**: https://cert-generator-10.preview.emergentagent.com/sample_certificate.png
- **Sample Sertifikat PDF**: https://cert-generator-10.preview.emergentagent.com/sample_certificate.pdf

### API Endpoints (Advanced):
```
POST /api/upload-template    → Upload template
POST /api/generate            → Generate certificates
GET  /api/certificates        → Get history
GET  /api/download-sample     → Download sample Excel
```

---

## 🎓 Video Tutorial (Coming Soon)

Segera tersedia video tutorial step-by-step!

---

## ❓ FAQ (Frequently Asked Questions)

**Q: Berapa maksimal peserta yang bisa digenerate sekaligus?**
A: Tidak ada limit, tapi disarankan <500 peserta per batch untuk performa optimal.

**Q: Bisa ganti font atau warna teks?**
A: Saat ini menggunakan font DejaVuSerif (fixed). Untuk customization lebih lanjut, hubungi developer.

**Q: Apakah data tersimpan di server?**
A: History tersimpan di MongoDB, tapi file sertifikat tidak disimpan permanent (hanya saat generate).

**Q: Bisa generate ulang dengan data yang sama?**
A: Ya, bisa upload file Excel yang sama lagi.

**Q: Support format lain selain PNG/PDF?**
A: Saat ini hanya PNG dan PDF. Format lain (JPG, SVG) belum didukung.

---

## 📞 Butuh Bantuan?

Jika ada pertanyaan atau menemukan bug, silakan hubungi tim support.

---

**Happy Generating! 🎉**

Made with ❤️ using FastAPI + React + MongoDB
