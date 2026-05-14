```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>VeloceSave</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap" rel="stylesheet">

  <style>
    *{
      margin:0;
      padding:0;
      box-sizing:border-box;
      font-family:'Cairo',sans-serif;
    }

    body{
      background:#f5f5f7;
      color:#111;
    }

    /* NAVBAR */
    .navbar{
      background:#07132c;
      padding:18px 7%;
      display:flex;
      justify-content:space-between;
      align-items:center;
    }

    .logo{
      font-size:38px;
      font-weight:800;
      color:white;
    }

    .logo span{
      color:#7b4dff;
    }

    .nav-links{
      display:flex;
      gap:35px;
    }

    .nav-links a{
      color:white;
      text-decoration:none;
      font-size:18px;
      transition:.3s;
    }

    .nav-links a:hover{
      color:#8f6bff;
    }

    /* HERO */
    .hero{
      text-align:center;
      padding:80px 20px;
    }

    .hero h1{
      font-size:70px;
      color:#3b3b9e;
      margin-bottom:15px;
      font-weight:800;
    }

    .hero p{
      color:#666;
      font-size:24px;
      margin-bottom:40px;
    }

    /* CONVERTER BOX */
    .converter-box{
      max-width:900px;
      margin:auto;
      background:white;
      border:2px solid #d9d0ff;
      border-radius:70px;
      display:flex;
      align-items:center;
      overflow:hidden;
      box-shadow:0 8px 25px rgba(0,0,0,0.06);
    }

    .converter-box input{
      flex:1;
      border:none;
      outline:none;
      padding:25px;
      font-size:18px;
      background:transparent;
    }

    .converter-box button{
      border:none;
      background:linear-gradient(45deg,#7b4dff,#b14dff);
      color:white;
      padding:22px 45px;
      font-size:20px;
      cursor:pointer;
      transition:.3s;
      border-radius:50px;
      margin:8px;
      font-weight:700;
    }

    .converter-box button:hover{
      transform:scale(1.05);
    }

    /* FEATURES */
    .features{
      display:flex;
      justify-content:center;
      gap:20px;
      flex-wrap:wrap;
      margin-top:35px;
    }

    .feature{
      background:white;
      border-radius:15px;
      padding:12px 22px;
      box-shadow:0 5px 15px rgba(0,0,0,0.05);
      font-weight:700;
      color:#555;
    }

    /* SECTION */
    .section{
      margin-top:100px;
      padding:0 10%;
      text-align:center;
    }

    .section h2{
      font-size:55px;
      margin-bottom:20px;
      color:#111827;
    }

    .section p{
      color:#666;
      line-height:2;
      font-size:20px;
      max-width:900px;
      margin:auto;
    }

    /* CARDS */
    .cards{
      margin-top:60px;
      display:grid;
      grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
      gap:30px;
    }

    .card{
      background:white;
      padding:35px;
      border-radius:25px;
      box-shadow:0 10px 25px rgba(0,0,0,0.06);
      transition:.3s;
    }

    .card:hover{
      transform:translateY(-8px);
    }

    .card h3{
      color:#4a3aff;
      margin-bottom:15px;
      font-size:28px;
    }

    .card p{
      font-size:18px;
    }

    /* FOOTER */
    footer{
      margin-top:120px;
      background:#07132c;
      color:white;
      text-align:center;
      padding:30px;
    }

    @media(max-width:768px){

      .hero h1{
        font-size:45px;
      }

      .hero p{
        font-size:18px;
      }

      .converter-box{
        flex-direction:column;
        border-radius:30px;
      }

      .converter-box button{
        width:90%;
      }

      .nav-links{
        display:none;
      }

      .section h2{
        font-size:35px;
      }

    }

  </style>
</head>
<body>

  <!-- NAVBAR -->
  <nav class="navbar">

    <div class="logo">
      Veloce<span>Save</span>
    </div>

    <div class="nav-links">
      <a href="#">يوتيوب إلى MP4</a>
      <a href="#">يوتيوب إلى MP3</a>
      <a href="#">تنزيل فيديوهات</a>
    </div>

  </nav>

  <!-- HERO -->
  <section class="hero">

    <h1>تحويل يوتيوب إلى MP3</h1>

    <p>
      حوّل فيديوهات يوتيوب إلى ملفات صوتية بجودة عالية خلال ثوانٍ.
    </p>

    <div class="converter-box">

      <input type="text" placeholder="الصق رابط يوتيوب هنا..." />

      <button>تحويل</button>

    </div>

    <div class="features">

      <div class="feature">⚡ سريع</div>
      <div class="feature">∞ بدون حدود</div>
      <div class="feature">🎁 مجاني</div>
      <div class="feature">☁ عبر الإنترنت</div>

    </div>

  </section>

  <!-- SECTION -->
  <section class="section">

    <h2>كيفية تنزيل ملفات MP3 من يوتيوب</h2>

    <p>
      انسخ رابط الفيديو من يوتيوب ثم الصقه داخل مربع التحويل واضغط على زر التحويل.
      بعد انتهاء المعالجة ستتمكن من تنزيل الملف الصوتي بسهولة وبأعلى جودة ممكنة.
    </p>

    <div class="cards">

      <div class="card">
        <h3>1. انسخ الرابط</h3>
        <p>
          قم بنسخ رابط فيديو يوتيوب الذي تريد تحويله.
        </p>
      </div>

      <div class="card">
        <h3>2. الصق الرابط</h3>
        <p>
          الصق الرابط داخل مربع التحويل في الأعلى.
        </p>
      </div>

      <div class="card">
        <h3>3. تحميل الملف</h3>
        <p>
          اضغط تحميل واحصل على ملف MP3 فوراً.
        </p>
      </div>

    </div>

  </section>

  <!-- FOOTER -->
  <footer>
    © 2026 VeloceSave - جميع الحقوق محفوظة
  </footer>

</body>
</html>
```
