<DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Quiz Spinner — MATH-UP 4 (Pink Theme)</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #ffc0cb;
      font-family: 'Poppins', sans-serif;
    }
    .card {
      background-color: #ffe6f0;
      border: none;
      border-radius: 15px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    textarea, input {
      background-color: #fff0f5 !important;
    }
    .btn-pink {
      background-color: #ff99cc;
      border: none;
      color: black;
    }
    .btn-pink:hover {
      background-color: #ff66b2;
      color: white;
    }
    #questionText {
      font-size: 2rem;
      text-align: center;
      font-weight: bold;
      min-height: 150px;
      background-color: #fff0f5;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
  </style>
</head>
<body class="container py-4">

  <h2 class="text-center fw-bold mb-4">🎯 Quiz Spinner — MATH-UP 4</h2>

  <div class="row">
    <!-- Daftar Soal -->
    <div class="col-md-5">
      <div class="card p-3 mb-4">
        <h5 class="fw-bold">Daftar Soal</h5>
        <ul id="questionList" class="list-group my-3"></ul>
        <div class="d-flex flex-wrap gap-2">
          <button class="btn btn-pink btn-sm" onclick="addQuestion()">Tambah</button>
          <button class="btn btn-pink btn-sm" onclick="addBulk()">Tambah Banyak</button>
          <button class="btn btn-pink btn-sm" onclick="editQuestion()">Edit</button>
          <button class="btn btn-pink btn-sm" onclick="deleteQuestion()">Hapus</button>
          <button class="btn btn-pink btn-sm" onclick="deleteAll()">Hapus Semua</button>
        </div>
      </div>
    </div>

    <!-- Tampilan Soal -->
    <div class="col-md-7">
      <div class="card p-3 text-center">
        <h5 id="resultLabel" class="fw-bold">Tekan SPIN untuk memilih soal</h5>
        <div id="questionText" class="my-3">-</div>
        <div class="d-flex justify-content-center gap-3">
          <button class="btn btn-pink" onclick="spin()">🎲 SPIN</button>
          <button class="btn btn-pink" onclick="showAnswer()">💡 Jawaban</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal Tambah Banyak -->
  <div class="modal fade" id="bulkModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content" style="background-color:#ffe6f0;">
        <div class="modal-header">
          <h5 class="modal-title">Tambah Banyak Soal</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <p>Masukkan soal dan jawaban (pisahkan dengan |, satu per baris):</p>
          <textarea id="bulkInput" class="form-control" rows="10"></textarea>
        </div>
        <div class="modal-footer">
          <button class="btn btn-pink" onclick="saveBulk()">Simpan Semua</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal Jawaban -->
  <div class="modal fade" id="answerModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content" style="background-color:#fff0f5;">
        <div class="modal-header">
          <h5 class="modal-title">Jawaban</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body text-center">
          <p id="answerText" class="fs-5 fw-bold"></p>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    let questions = JSON.parse(localStorage.getItem("questions")) || [
      { q: "Berapakah 12 × 8?", a: "96" },
      { q: "Hitung 345 + 678.", a: "1023" },
      { q: "Jika 1/2 + 1/3 = ?", a: "5/6" },
      { q: "Konversi 0.25 ke pecahan.", a: "1/4" },
      { q: "Berapa KPK dari 6 dan 8?", a: "24" }
    ];
    let selectedIndex = null;

    function saveData() {
      localStorage.setItem("questions", JSON.stringify(questions));
    }

    function renderList() {
      const list = document.getElementById("questionList");
      list.innerHTML = "";
      questions.forEach((q, i) => {
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.textContent = `${i+1}. ${q.q}`;
        li.onclick = () => {
          document.querySelectorAll("#questionList li").forEach(e => e.classList.remove("active"));
          li.classList.add("active");
          selectedIndex = i;
        };
        list.appendChild(li);
      });
    }

    function addQuestion() {
      const q = prompt("Masukkan teks soal:");
      if (!q) return;
      const a = prompt("Masukkan jawaban:");
      if (!a) return;
      questions.push({ q, a });
      saveData();
      renderList();
    }

    function addBulk() {
      new bootstrap.Modal(document.getElementById('bulkModal')).show();
    }

    function saveBulk() {
      const text = document.getElementById("bulkInput").value.trim();
      if (!text) return alert("Tidak ada input!");
      const lines = text.split("\n");
      let added = 0;
      lines.forEach(line => {
        const parts = line.split("|");
        if (parts.length === 2) {
          const [q, a] = parts.map(x => x.trim());
          if (q && a) {
            questions.push({ q, a });
            added++;
          }
        }
      });
      saveData();
      renderList();
      document.getElementById("bulkInput").value = "";
      bootstrap.Modal.getInstance(document.getElementById('bulkModal')).hide();
      alert(`${added} soal berhasil ditambahkan!`);
    }

    function editQuestion() {
      if (selectedIndex === null) return alert("Pilih soal dulu!");
      const q = prompt("Edit soal:", questions[selectedIndex].q);
      if (q === null) return;
      const a = prompt("Edit jawaban:", questions[selectedIndex].a);
      if (a === null) return;
      questions[selectedIndex] = { q, a };
      saveData();
      renderList();
    }

    function deleteQuestion() {
      if (selectedIndex === null) return alert("Pilih soal yang mau dihapus!");
      if (confirm("Hapus soal ini?")) {
        questions.splice(selectedIndex, 1);
        selectedIndex = null;
        saveData();
        renderList();
      }
    }

    function deleteAll() {
      if (confirm("Hapus SEMUA soal?")) {
        questions = [];
        saveData();
        renderList();
      }
    }

    function spin() {
      if (questions.length === 0) return alert("Belum ada soal!");
      selectedIndex = Math.floor(Math.random() * questions.length);
      document.getElementById("resultLabel").textContent = `Soal terpilih (No ${selectedIndex+1})`;
      document.getElementById("questionText").textContent = questions[selectedIndex].q;
    }

    function showAnswer() {
      if (selectedIndex === null) return alert("Belum ada soal dipilih!");
      document.getElementById("answerText").textContent = questions[selectedIndex].a;
      new bootstrap.Modal(document.getElementById('answerModal')).show();
    }

    renderList();
  </script>
</body>
</html>
