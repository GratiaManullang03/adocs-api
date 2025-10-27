# [NAMA APLIKASI] - [Deskripsi Singkat]

## Deskripsi Sistem
[Jelaskan secara singkat apa fungsi utama aplikasi ini, siapa yang menggunakannya, dan masalah apa yang diselesaikan]

---

## Autentikasi & Otorisasi

### Sistem Autentikasi
- **Metode**: [JWT / Session / OAuth / API Key / dll]
- **Header Required**: [Contoh: Authorization: Bearer <token>]
- **Token Location**: [Header / Cookie / Query Parameter]
- **Validasi**: [Jelaskan bagaimana token divalidasi]

### Role & Permission
Sistem memiliki beberapa role pengguna:
- **[Role 1]**: [Deskripsi akses dan permission]
- **[Role 2]**: [Deskripsi akses dan permission]
- **[Role 3]**: [Deskripsi akses dan permission]

---

## Fitur & Endpoint

### 1. [Kategori Fitur - Contoh: Authentication]

#### [METHOD] /api/[endpoint-path]
**Fungsi**: [Jelaskan apa yang dilakukan endpoint ini]
**Auth Required**: [Ya/Tidak] ([Role yang boleh akses jika perlu auth])
**Request Body**:
```json
{
  "field1": "type (required/optional) - deskripsi",
  "field2": "type (required/optional) - deskripsi"
}
```

**Query Parameters** (jika ada):
- `param1`: type (default: value) - deskripsi
- `param2`: type (optional) - deskripsi

**Path Parameters** (jika ada):
- `id`: type (required) - deskripsi

**Validasi Auth**:
- [Syarat autentikasi 1]
- [Syarat autentikasi 2]

**Validasi Data**:
- [Aturan validasi field 1]
- [Aturan validasi field 2]
- [Logika bisnis yang harus dipenuhi]

**Response Success ([Status Code])**:
```json
{
  "success": true,
  "message": "Pesan sukses",
  "data": {
    // Structure response
  }
}
```

**Response Error**:
- [Status Code]: [Kondisi error]
- [Status Code]: [Kondisi error]
- [Status Code]: [Kondisi error]

**Logika Khusus** (jika ada):
- [Jelaskan logika bisnis khusus yang perlu dipahami]
- [Contoh: perhitungan, algoritma, kondisi khusus]

---

#### [Tambahkan endpoint lainnya dengan format yang sama]

---

### 2. [Kategori Fitur Berikutnya]

[Ulangi format endpoint di atas untuk setiap endpoint dalam kategori ini]

---

## Flow Aplikasi

### 1. Flow [Nama Flow - Contoh: Login User]
```
[Step 1: Aksi User]
  ↓
[Step 2: Proses/Validasi]
  ↓
[Step 3: Kondisi]
  ↓
If [Kondisi A]:
  → [Aksi 1]
  → [Aksi 2]
  → [Result]

If [Kondisi B]:
  → [Aksi Alternatif 1]
  → [Aksi Alternatif 2]
  → [Result Alternatif]
```

### 2. Flow [Nama Flow Berikutnya]
```
[Jelaskan flow dengan diagram sederhana menggunakan arrow]
```

---

## Data Models / Schema

### [Nama Model 1]
```
{
  "field1": "type - deskripsi",
  "field2": "type - deskripsi",
  "field3": {
    "nestedField1": "type - deskripsi",
    "nestedField2": "type - deskripsi"
  },
  "field4": "[array of objects] - deskripsi"
}
```

**Relationships** (jika ada):
- [Relasi dengan model lain]

**Validations**:
- [Aturan validasi untuk fields]

---

## Status & State Management

### [Nama Status Type - Contoh: Order Status]
- **[status1]**: [Deskripsi kapan status ini muncul]
- **[status2]**: [Deskripsi kapan status ini muncul]
- **[status3]**: [Deskripsi kapan status ini muncul]

### Status Determination Logic
```
If [kondisi 1]:
  → status = "[status1]"

If [kondisi 2]:
  → status = "[status2]"

If [kondisi 3]:
  → status = "[status3]"
```

---

## Response Format Standar

### Success Response
```json
{
  "success": true,
  "message": "Pesan sukses (optional)",
  "data": {
    // Data yang dikembalikan
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Pesan error yang jelas",
  "errors": [
    {
      "field": "namaField",
      "message": "Pesan error untuk field ini"
    }
  ]
}
```

### Pagination Response (jika ada)
```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 100,
      "totalPages": 10
    }
  }
}
```

---

## HTTP Status Codes

- **200**: OK - [Kapan digunakan]
- **201**: Created - [Kapan digunakan]
- **400**: Bad Request - [Kapan digunakan]
- **401**: Unauthorized - [Kapan digunakan]
- **403**: Forbidden - [Kapan digunakan]
- **404**: Not Found - [Kapan digunakan]
- **409**: Conflict - [Kapan digunakan]
- **422**: Unprocessable Entity - [Kapan digunakan]
- **500**: Internal Server Error - [Kapan digunakan]

---

## Panduan untuk AI Frontend Developer

### 1. Autentikasi
- [Instruksi khusus cara handle auth]
- [Cara simpan token]
- [Cara handle expired token]
- [Cara handle error auth]

### 2. Form Handling
- [Instruksi validasi frontend]
- [Cara handle form errors]
- [Best practice untuk form submission]

### 3. [Feature-Specific Guidelines]
- [Instruksi khusus untuk fitur tertentu]
- [Edge cases yang perlu dihandle]
- [Best practice untuk UX]

### 4. State Management
- [Data apa yang perlu disimpan di state]
- [Kapan harus refresh data]
- [Cara handle optimistic updates]

### 5. UI/UX Guidelines
- [Instruksi tampilan untuk setiap state]
- [Loading states]
- [Error states]
- [Empty states]
- [Success feedback]

### 6. Role-Based Rendering
- [Instruksi show/hide berdasarkan role]
- [Handle unauthorized access]
- [Menu/fitur untuk setiap role]

### 7. Performance Tips
- [Optimization yang perlu dilakukan]
- [Caching strategy]
- [Debouncing/Throttling]
- [Lazy loading]

---

## Business Rules & Constraints

### [Kategori Rules 1]
- [Rule 1]: [Penjelasan detail]
- [Rule 2]: [Penjelasan detail]
- [Rule 3]: [Penjelasan detail]

### [Kategori Rules 2]
- [Rule 1]: [Penjelasan detail]
- [Rule 2]: [Penjelasan detail]

---

## Error Handling Best Practice

### Common Errors & Solutions
1. **[Error Type 1]**
   - **Cause**: [Penyebab]
   - **Solution**: [Cara handle di frontend]
   - **User Message**: [Pesan yang ditampilkan ke user]

2. **[Error Type 2]**
   - **Cause**: [Penyebab]
   - **Solution**: [Cara handle di frontend]
   - **User Message**: [Pesan yang ditampilkan ke user]

### Error Handling Strategy
- [Instruksi umum error handling]
- [Logging strategy]
- [Fallback UI]
- [Retry mechanism]

---

## Integration Notes

### External Services (jika ada)
- **[Service Name]**: [Purpose dan cara integrasinya]
- **[Service Name]**: [Purpose dan cara integrasinya]

### Webhooks (jika ada)
- **[Webhook Name]**: [Kapan triggered dan payload yang dikirim]

### Background Jobs (jika ada)
- **[Job Name]**: [Apa yang dilakukan dan kapan dijalankan]

---

## Testing Guidelines

### Test Scenarios
1. **[Feature/Endpoint Name]**
   - [ ] [Test case 1]
   - [ ] [Test case 2]
   - [ ] [Test case 3]
   - [ ] [Edge case 1]
   - [ ] [Edge case 2]

### Mock Data
[Contoh data untuk testing]

---

## Catatan Tambahan

### Keamanan
- [Security considerations]
- [Best practices]
- [What to avoid]

### Performance
- [Performance tips]
- [Optimization strategies]

### Limitations
- [Batasan sistem yang perlu diketahui]
- [Known issues]
- [Workarounds]

---

## Changelog / Version History (Optional)

### Version [X.X.X] - [Date]
- [Changes made]
- [New features]
- [Bug fixes]
- [Breaking changes]

---

## Glossary (Optional)

- **[Term 1]**: [Definisi]
- **[Term 2]**: [Definisi]
- **[Term 3]**: [Definisi]

---

## Contact & Support

- **Developer**: [Nama/Team]
- **Documentation**: [Link]
- **API Base URL**: [URL]
- **Environment**: [Development/Staging/Production]
