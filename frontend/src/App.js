import { useState, useEffect } from "react";
import "@/App.css";
import axios from "axios";
import { Upload, FileText, Download, CheckCircle, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [templateFile, setTemplateFile] = useState(null);
  const [excelFile, setExcelFile] = useState(null);
  const [certificates, setCertificates] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchCertificates();
  }, []);

  const fetchCertificates = async () => {
    try {
      const response = await axios.get(`${API}/certificates`);
      setCertificates(response.data);
    } catch (error) {
      console.error("Error fetching certificates:", error);
    }
  };

  const handleTemplateUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setTemplateFile(file);
    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      await axios.post(`${API}/upload-template`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      toast.success("Template berhasil diupload!");
    } catch (error) {
      toast.error("Gagal upload template: " + error.response?.data?.detail);
    } finally {
      setUploading(false);
    }
  };

  const handleExcelChange = (e) => {
    setExcelFile(e.target.files[0]);
  };

  const handleGenerate = async () => {
    if (!excelFile) {
      toast.error("Silakan pilih file Excel/CSV terlebih dahulu");
      return;
    }

    setGenerating(true);

    try {
      const formData = new FormData();
      formData.append("file", excelFile);

      const response = await axios.post(`${API}/generate`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob",
      });

      // Download ZIP file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `certificates_${Date.now()}.zip`);
      document.body.appendChild(link);
      link.click();
      link.remove();

      toast.success("Sertifikat berhasil digenerate!");
      fetchCertificates();
      setExcelFile(null);
    } catch (error) {
      toast.error("Gagal generate sertifikat: " + (error.response?.data?.detail || error.message));
    } finally {
      setGenerating(false);
    }
  };

  const handleDownloadSample = () => {
    window.open(`${API}/download-sample`, '_blank');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50">
      <div className="container mx-auto px-4 py-12 max-w-7xl">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl lg:text-6xl font-bold mb-4 bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent" style={{ fontFamily: "'Playfair Display', serif" }}>
            Generator Sertifikat Otomatis
          </h1>
          <p className="text-lg text-gray-600" style={{ fontFamily: "'Inter', sans-serif" }}>
            Buat sertifikat pelatihan secara massal dengan mudah dan cepat
          </p>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {/* Upload Section */}
          <Card data-testid="upload-card" className="border-2 border-emerald-100 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader className="bg-gradient-to-r from-emerald-50 to-teal-50">
              <CardTitle className="flex items-center gap-2 text-2xl" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                <Upload className="w-6 h-6 text-emerald-600" />
                Upload Template & Data
              </CardTitle>
              <CardDescription className="text-base">
                Upload template sertifikat dan file Excel/CSV berisi data peserta
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6 pt-6">
              {/* Template Upload */}
              <div className="space-y-3">
                <label className="block text-sm font-semibold text-gray-700">
                  1. Upload Template Sertifikat (PNG)
                </label>
                <div className="relative">
                  <input
                    data-testid="template-upload-input"
                    type="file"
                    accept=".png,.jpg,.jpeg"
                    onChange={handleTemplateUpload}
                    className="hidden"
                    id="template-upload"
                  />
                  <label
                    htmlFor="template-upload"
                    className="flex items-center justify-center gap-2 p-6 border-2 border-dashed border-emerald-300 rounded-xl cursor-pointer hover:border-emerald-500 hover:bg-emerald-50 transition-all duration-200"
                  >
                    <FileText className="w-5 h-5 text-emerald-600" />
                    <span className="text-sm font-medium text-gray-700">
                      {templateFile ? templateFile.name : "Klik untuk pilih template"}
                    </span>
                  </label>
                </div>
                {uploading && (
                  <p className="text-sm text-emerald-600 flex items-center gap-2">
                    <Clock className="w-4 h-4 animate-spin" />
                    Mengupload...
                  </p>
                )}
                {templateFile && !uploading && (
                  <p className="text-sm text-emerald-600 flex items-center gap-2">
                    <CheckCircle className="w-4 h-4" />
                    Template berhasil diupload
                  </p>
                )}
              </div>

              {/* Excel Upload */}
              <div className="space-y-3">
                <label className="block text-sm font-semibold text-gray-700">
                  2. Upload Data Peserta (Excel/CSV)
                </label>
                <div className="relative">
                  <input
                    data-testid="excel-upload-input"
                    type="file"
                    accept=".xlsx,.xls,.csv"
                    onChange={handleExcelChange}
                    className="hidden"
                    id="excel-upload"
                  />
                  <label
                    htmlFor="excel-upload"
                    className="flex items-center justify-center gap-2 p-6 border-2 border-dashed border-teal-300 rounded-xl cursor-pointer hover:border-teal-500 hover:bg-teal-50 transition-all duration-200"
                  >
                    <FileText className="w-5 h-5 text-teal-600" />
                    <span className="text-sm font-medium text-gray-700">
                      {excelFile ? excelFile.name : "Klik untuk pilih file Excel/CSV"}
                    </span>
                  </label>
                </div>
                <p className="text-xs text-gray-500">
                  File harus memiliki kolom: <strong>name</strong>, <strong>course</strong>, <strong>date</strong>
                </p>
              </div>

              {/* Generate Button */}
              <Button
                data-testid="generate-button"
                onClick={handleGenerate}
                disabled={!excelFile || generating}
                className="w-full py-6 text-lg font-semibold bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {generating ? (
                  <>
                    <Clock className="w-5 h-5 mr-2 animate-spin" />
                    Sedang Generate...
                  </>
                ) : (
                  <>
                    <Download className="w-5 h-5 mr-2" />
                    Generate Sertifikat
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Instructions */}
          <Card data-testid="instructions-card" className="border-2 border-teal-100 shadow-lg">
            <CardHeader className="bg-gradient-to-r from-teal-50 to-cyan-50">
              <CardTitle className="text-2xl" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                Panduan Penggunaan
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">1. Persiapkan Template</h3>
                  <p className="text-sm text-gray-600">
                    Template sertifikat dalam format PNG dengan ukuran 3000×2000 px (landscape)
                  </p>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">2. Format File Excel/CSV</h3>
                  <p className="text-sm text-gray-600 mb-2">File harus memiliki 3 kolom:</p>
                  <ul className="text-sm text-gray-600 space-y-1 list-disc list-inside">
                    <li><strong>name</strong> - Nama peserta</li>
                    <li><strong>course</strong> - Nama pelatihan</li>
                    <li><strong>date</strong> - Tanggal (format: YYYY-MM-DD atau DD/MM/YYYY)</li>
                  </ul>
                  <Button
                    data-testid="download-sample-button"
                    onClick={handleDownloadSample}
                    variant="outline"
                    size="sm"
                    className="mt-3 text-emerald-600 border-emerald-300 hover:bg-emerald-50"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download Contoh Excel
                  </Button>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">3. Hasil Generate</h3>
                  <p className="text-sm text-gray-600">
                    Sistem akan menghasilkan file ZIP berisi sertifikat dalam format PNG dan PDF untuk setiap peserta
                  </p>
                </div>

                <div className="bg-gradient-to-r from-emerald-50 to-teal-50 p-4 rounded-lg border border-emerald-200">
                  <p className="text-sm text-gray-700">
                    <strong>Catatan:</strong> Semua teks akan di-center dan QR code akan ditambahkan secara otomatis
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* History Section */}
        <Card data-testid="history-card" className="border-2 border-cyan-100 shadow-lg">
          <CardHeader className="bg-gradient-to-r from-cyan-50 to-blue-50">
            <CardTitle className="text-2xl" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
              Riwayat Generate
            </CardTitle>
            <CardDescription>Daftar sertifikat yang telah digenerate</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            {certificates.length === 0 ? (
              <p className="text-center text-gray-500 py-8">Belum ada sertifikat yang digenerate</p>
            ) : (
              <div className="space-y-3">
                {certificates.map((cert, idx) => (
                  <div
                    key={cert.id}
                    data-testid={`certificate-item-${idx}`}
                    className="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg border border-gray-200 hover:shadow-md transition-all duration-200"
                  >
                    <div className="flex items-center gap-3">
                      <CheckCircle className="w-5 h-5 text-emerald-600" />
                      <div>
                        <p className="font-semibold text-gray-800">{cert.filename}</p>
                        <p className="text-sm text-gray-600">
                          {cert.participant_count} peserta • {new Date(cert.created_at).toLocaleDateString('id-ID')}
                        </p>
                      </div>
                    </div>
                    <span className="px-3 py-1 bg-emerald-100 text-emerald-700 text-xs font-semibold rounded-full">
                      {cert.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default App;