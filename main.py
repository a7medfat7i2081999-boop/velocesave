import os
from flask import Flask, request, render_template_string, redirect, send_from_directory
import subprocess

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VeloceSave - تنزيل الفيديوهات السريع</title>
    <link rel="icon" type="image/png" href="/logo.png">

    <style>
        html, body { height: 100%; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #F9FAFB; color: #1F2937; }
        .progress-container { position: fixed; top: 0; left: 0; width: 100%; height: 6px; background: #E5E7EB; z-index: 10000; }
        .progress-bar { height: 100%; width: 0%; background: #7C3AED; transition: width 0.4s ease; }
        .top-navbar { display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; box-sizing: border-box; }
        .logo-text { font-size: 32px; font-weight: 900; letter-spacing: -1px; background: linear-gradient(135deg, #7C3AED, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: sans-serif; }
        .lang-select { padding: 8px 16px; border: 2px solid #E5E7EB; border-radius: 10px; background: white; color: #4B5563; font-weight: 600; cursor: pointer; font-size: 14px; outline: none; }
        .wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh; padding: 20px; box-sizing: border-box; }
        .container { background: #FFFFFF; padding: 50px 40px; border-radius: 24px; box-shadow: 0 10px 30px rgba(124, 58, 237, 0.06); max-width: 600px; width: 100%; border: 1px solid #E5E7EB; text-align: center; }
        h1 { color: #111827; font-size: 28px; font-weight: 800; margin-top: 0; margin-bottom: 12px; }
        p.subtitle { color: #6B7280; font-size: 16px; margin-bottom: 35px; margin-top: 0; }
        .counter-badge { display: inline-block; background: rgba(124, 58, 237, 0.1); color: #7C3AED; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 14px; margin-bottom: 20px; }
        input { width: 100%; padding: 18px 20px; background: #F3F4F6; border: 2px solid #E5E7EB; border-radius: 14px; color: #111827; box-sizing: border-box; font-size: 16px; text-align: left; transition: all 0.3s; margin-bottom: 25px; }
        input:focus { border-color: #7C3AED; background: #FFFFFF; outline: none; box-shadow: 0 0 12px rgba(124, 58, 237, 0.15); }
        .options { display: flex; justify-content: space-between; margin-bottom: 30px; gap: 12px; }
        .option-card { flex: 1; background: #F3F4F6; border: 2px solid transparent; padding: 14px; border-radius: 12px; cursor: pointer; font-weight: 700; color: #4B5563; transition: all 0.3s; text-align: center; }
        .option-card.active { border-color: #7C3AED; background: rgba(124, 58, 237, 0.08); color: #7C3AED; }
        button { width: 100%; padding: 18px; background: #7C3AED; color: white; border: none; border-radius: 14px; font-size: 18px; font-weight: bold; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3); }
        button:hover { background: #6D28D9; transform: translateY(-2px); }
        .features-grid { display: flex; justify-content: space-between; gap: 10px; margin-top: 30px; }
        .feature-badge { flex: 1; background: #F9FAFB; border: 1px solid #E5E7EB; padding: 12px 5px; border-radius: 10px; font-size: 14px; font-weight: 600; color: #4B5563; }
        .welcome-section { max-width: 600px; width: 100%; margin: 40px auto 0 auto; background: white; border: 1px solid #E5E7EB; padding: 30px; border-radius: 20px; text-align: right; box-shadow: 0 4px 20px rgba(0,0,0,0.02); }
        .welcome-section p { font-size: 15px; color: #4B5563; line-height: 1.8; margin: 0; }
        .paywall { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(11, 14, 23, 0.98); z-index: 99999; justify-content: center; align-items: center; color: white; flex-direction: column; padding: 20px; text-align: center; box-sizing: border-box; }
        .auth-box { background: #1F2937; padding: 40px; border-radius: 20px; max-width: 400px; width: 100%; border: 1px solid #374151; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        .auth-box h2 { font-size: 24px; color: #EF4444; margin-top: 0; margin-bottom: 10px; }
        .auth-box p { color: #9CA3AF; font-size: 14px; margin-bottom: 25px; }
        .auth-box input { background: #374151; border-color: #4B5563; color: white; margin-bottom: 15px; padding: 14px; text-align: right; }
        .auth-box input::placeholder { color: #9CA3AF; }
        .auth-box input:focus { border-color: #8B5CF6; background: #374151; }
        .auth-btn { width: 100%; padding: 14px; background: #7C3AED; color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s; }
        .auth-btn:hover { background: #6D28D9; }
    </style>
</head>
<body>
    <div class="progress-container"><div class="progress-bar" id="topProgressBar"></div></div>
    <div class="paywall" id="paywallZone">
        <div class="auth-box">
            <h2 id="paywallTitle">⚠️ انتهت المحاولات المجانية!</h2>
            <p id="paywallText">لديك 15 محاولة مجانية قبل تسجيل الدخول. يرجى تسجيل الدخول أو إنشاء حساب الآن لمتابعة تحميل فيديوهاتك.</p>
            <form onsubmit="handleLogin(event)">
                <input type="email" placeholder="البريد الإلكتروني" required>
                <input type="password" placeholder="كلمة المرور" required>
                <button type="submit" class="auth-btn">تسجيل الدخول / إنشاء حساب</button>
            </form>
        </div>
    </div>
    <div class="top-navbar">
        <div class="logo-text">VeloceSave</div>
        <select class="lang-select" onchange="changeLanguage(this.value)">
            <option value="ar">العربية</option>
            <option value="en">English</option>
            <option value="es">Español</option>
            <option value="fr">Français</option>
            <option value="tr">Türkçe</option>
            <option value="de">Deutsch</option>
            <option value="zh">中文</option>
        </select>
    </div>
    <div class="wrapper">
        <div class="container">
            <div class="counter-badge" id="limitBadge">متبقي لك 15 محاولة مجانية</div>
            <h1 id="mainTitle">تنزيل الفيديوهات السريع</h1>
            <p class="subtitle" id="mainSubtitle">نزّل فيديوهاتك بصيغة MP3 أو MP4 عبر الإنترنت مجاناً</p>
            <form id="downloadForm" onsubmit="handleDownload(event)">
                <input type="url" id="videoUrl" placeholder="الصق رابط الفيديو هنا..." required>
                <div class="options">
                    <div class="option-card active" id="opt-mp4" onclick="setFormat('best')">فيديو MP4</div>
                    <div class="option-card" id="opt-mp3" onclick="setFormat('mp3')">صوت MP3</div>
                </div>
                <input type="hidden" id="videoFormat" value="best">
                <button type="submit" id="btnText">تـنـزيـل</button>
            </form>
            <div class="features-grid">
                <div class="feature-badge" id="f1">سهل</div>
                <div class="feature-badge" id="f2">مجاني</div>
                <div class="feature-badge" id="f3">بلا حدود</div>
                <div class="feature-badge" id="f4">لا يحتاج التنزيل</div>
            </div>
        </div>
        <div class="welcome-section">
            <p id="welcomeParagraph">
                اهلا بك في محمل الفيديوهات السريع ما عليك سوي لصق الرابط فيه مربع الURL ثم ضغط تحميل نحن سعداء جدا لانك تستخدم موقعنا ونأمل ان يكون عجبك لديك ١٥ محاولة مجانية بدون تسجيل دخول لتنزيل الفيدوهات وبعدها تنتقل للحساب المدفوع ويجب تسجيل الدخول شكرا لك حقا انك تستخدم خدمتنا
            </p>
        </div>
    </div>
    <script>
        const translations = {
            ar: {
                badge: "متبقي لك {r} محاولة مجانية",
                title: "تنزيل الفيديوهات السريع",
                subtitle: "نزّل فيديوهاتك بصيغة MP3 أو MP4 عبر الإنترنت مجاناً",
                btn: "تـنـزيـل",
                f1: "سهل", f2: "مجاني", f3: "بلا حدود", f4: "لا يحتاج التنزيل",
                welcome: "اهلا بك في محمل الفيديوهات السريع ما عليك سوي لصق الرابط فيه مربع الURL ثم ضغط تحميل نحن سعداء جدا لانك تستخدم موقعنا ونأمل ان يكون عجبك لديك ١٥ محاولة مجانية بدون تسجيل دخول لتنزيل الفيدوهات وبعدها تنتقل للحساب المدفوع ويجب تسجيل الدخول شكرا لك حقا انك تستخدم خدمتنا",
                pTitle: "⚠️ انتهت المحاولات المجانية!",
                pText: "لديك 15 محاولة مجانية قبل تسجيل الدخول. يرجى تسجيل الدخول أو إنشاء حساب الآن لمتابعة تحميل فيديوهاتك."
            },
            en: {
                badge: "{r} free downloads remaining",
                title: "Fast Video Downloader",
                subtitle: "Download your favorite videos as MP3 or MP4 online for free",
                btn: "Download",
                f1: "Easy", f2: "Free", f3: "Unlimited", f4: "No Install",
                welcome: "Welcome to our fast video downloader! Just paste the link into the URL box and click download. We are very happy you are using our website and hope you like it. You have 15 free attempts without logging in, after which you transfer to the paid account and must log in. Thank you truly for using our service.",
                pTitle: "⚠️ Free limits reached!",
                pText: "You have 15 free downloads before logging in. Please log in or create an account to continue downloading."
            }
        };
        let currentLang = 'ar';
        let downloadsCount = localStorage.getItem('user_downloads') ? parseInt(localStorage.getItem('user_downloads')) : 0;
        let isLoggedIn = localStorage.getItem('user_logged_in') === 'true';
        updateUIElements();
        function setFormat(fmt) {
            document.getElementById('videoFormat').value = fmt;
            document.getElementById('opt-mp4').classList.remove('active');
            document.getElementById('opt-mp3').classList.remove('active');
            if(fmt === 'best') { document.getElementById('opt-mp4').classList.add('active'); } else { document.getElementById('opt-mp3').classList.add('active'); }
        }
        function changeLanguage(lang) {
            currentLang = translations[lang] ? lang : 'en';
            document.body.dir = currentLang === 'ar' ? "rtl" : "ltr";
            updateUIElements();
        }
        function handleDownload(e) {
            e.preventDefault();
            if (!isLoggedIn && downloadsCount >= 15) { document.getElementById('paywallZone').style.display = 'flex'; return; }
            var url = document.getElementById('videoUrl').value;
            var fmt = document.getElementById('videoFormat').value;
            if(!url) return;
            if (!isLoggedIn) { downloadsCount++; localStorage.setItem('user_downloads', downloadsCount); }
            updateUIElements();
            var downloadUrl = '/download?url=' + encodeURIComponent(url) + '&format=' + fmt;
            window.open(downloadUrl, '_blank');
            if (!isLoggedIn && downloadsCount >= 15) { setTimeout(() => { document.getElementById('paywallZone').style.display = 'flex'; }, 1000); }
        }
        function handleLogin(e) {
            e.preventDefault();
            localStorage.setItem('user_logged_in', 'true');
            isLoggedIn = true;
            document.getElementById('paywallZone').style.display = 'none';
            alert('تم تسجيل الدخول بنجاح! يمكنك الآن الاستمرار في التحميل.');
            updateUIElements();
        }
        function updateUIElements() {
            let percentage = (downloadsCount / 15) * 100;
            if (isLoggedIn) percentage = 0; 
            document.getElementById('topProgressBar').style.width = percentage + '%';
            let remaining = 15 - downloadsCount;
            if (remaining < 0 || isLoggedIn) remaining = 0;
            let data = translations[currentLang] || translations['en'];
            if (isLoggedIn) { document.getElementById('limitBadge').innerText = "وضع الحساب النشط ✨"; document.getElementById('paywallZone').style.display = 'none'; } else { document.getElementById('limitBadge').innerText = data.badge.replace("{r}", remaining); }
            document.getElementById('mainTitle').innerText = data.title;
            document.getElementById('mainSubtitle').innerText = data.subtitle;
            document.getElementById('btnText').innerText = data.btn;
            document.getElementById('f1').innerText = data.f1;
            document.getElementById('f2').innerText = data.f2;
            document.getElementById('f3').innerText = data.f3;
            document.getElementById('f4').innerText = data.f4;
            document.getElementById('welcomeParagraph').innerText = data.welcome;
            document.getElementById('paywallTitle').innerText = data.pTitle;
            document.getElementById('paywallText').innerText = data.pText;
            if (!isLoggedIn && downloadsCount >= 15) { document.getElementById('paywallZone').style.display = 'flex'; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/logo.png')
def favicon():
    return send_from_directory(os.getcwd(), 'logo.png', mimetype='image/png')

@app.route('/download')
def download():
    video_url = request.args.get('url')
    fmt = request.args.get('format', 'best')
    if not video_url:
        return "الرابط مطلوب", 400
    try:
        if fmt == 'mp3':
            command = f'yt-dlp -g -f "ba" "{video_url}"'
        else:
            command = f'yt-dlp -g -f "best" "{video_url}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        direct_link = result.stdout.strip()
        if direct_link:
            return redirect(direct_link)
        else:
            return "فشل استخراج الرابط، تأكد من صحته", 400
    except Exception as e:
        return f"خطأ في النظام: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
