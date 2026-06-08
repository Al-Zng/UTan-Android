import os

BASE = "utan_flutter"

# إنشاء كل المجلدات
dirs = [
    f"{BASE}/lib/models",
    f"{BASE}/lib/services",
    f"{BASE}/lib/screens",
    f"{BASE}/lib/widgets",
    f"{BASE}/android/app/src/main/res/xml",
    f"{BASE}/android/app/src/main",
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# 1. pubspec.yaml
pubspec = '''name: utan_flutter
description: UTan – Full Android replica of iOS version
publish_to: 'none'
version: 3.0.4+9

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6
  shared_preferences: ^2.2.2
  http: ^1.2.1  # Updated version
  video_player: ^2.8.1
  path_provider: ^2.1.1
  dio: ^5.3.3
  gallery_saver: ^2.3.2
  google_fonts: ^6.1.0
  cached_network_image: ^3.3.0

dependency_overrides:
  http: ^1.2.1  # Added override to solve version conflict

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
'''
with open(f"{BASE}/pubspec.yaml", "w", encoding="utf-8") as f:
    f.write(pubspec)

# 2. network_security_config.xml
# ✅ FIX: يسمح بكل الـ HTTP/HTTPS دون قيود + يثق بكل الـ CA
network_security = '''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
        </trust-anchors>
    </base-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">movie.vodu.me</domain>
        <domain includeSubdomains="true">vodu.me</domain>
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
        </trust-anchors>
    </domain-config>
</network-security-config>
'''
os.makedirs(f"{BASE}/android/app/src/main/res/xml", exist_ok=True)
with open(f"{BASE}/android/app/src/main/res/xml/network_security_config.xml", "w", encoding="utf-8") as f:
    f.write(network_security)

# 3. AndroidManifest.xml
# ✅ FIX: usesCleartextTraffic="true" + networkSecurityConfig + الصلاحيات الصحيحة
android_manifest = '''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="29"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="32"/>
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO"/>
    <application
        android:label="UTan"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher"
        android:usesCleartextTraffic="true"
        android:networkSecurityConfig="@xml/network_security_config"
        android:requestLegacyExternalStorage="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            <meta-data
              android:name="io.flutter.embedding.android.NormalTheme"
              android:resource="@style/NormalTheme"
              />
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        <meta-data android:name="flutterEmbedding" android:value="2" />
    </application>
</manifest>
'''
with open(f"{BASE}/android/app/src/main/AndroidManifest.xml", "w", encoding="utf-8") as f:
    f.write(android_manifest)

# 4. main.dart
# ✅ FIX: HttpOverrides محسّن + IOClient صريح يتجاوز SSL بشكل موثوق على Android
main_dart = '''import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/home_screen.dart';
import 'screens/browse_screen.dart';
import 'screens/search_screen.dart';
import 'screens/downloads_screen.dart';
import 'screens/settings_screen.dart';
import 'services/settings_store.dart';
import 'services/progress_store.dart';
import 'services/favorites_store.dart';
import 'services/download_manager.dart';

// ✅ FIX: تجاوز شامل لكل SSL/TLS على Android
class InsecureHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    final client = super.createHttpClient(context);
    client.badCertificateCallback =
        (X509Certificate cert, String host, int port) => true;
    client.connectionTimeout = const Duration(seconds: 30);
    return client;
  }
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // ✅ FIX: يجب أن يُضبط قبل أي طلب شبكة
  HttpOverrides.global = InsecureHttpOverrides();
  await SettingsStore().init();
  await WatchProgressStore().init();
  await FavoritesStore().init();
  await DownloadManager().init();
  runApp(const UTanApp());
}

class UTanApp extends StatelessWidget {
  const UTanApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'UTan',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0D0517),
        primaryColor: const Color(0xFFE50914),
        textTheme: GoogleFonts.rubikTextTheme(ThemeData.dark().textTheme).apply(
          bodyColor: Colors.white,
          displayColor: Colors.white,
        ),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFFE50914),
          surface: Color(0xFF1C1C24),
          background: Color(0xFF0D0517),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0D0517),
          elevation: 0,
          centerTitle: true,
        ),
        useMaterial3: true,
      ),
      home: const MainTabView(),
    );
  }
}

class MainTabView extends StatefulWidget {
  const MainTabView({super.key});
  @override
  State<MainTabView> createState() => _MainTabViewState();
}

class _MainTabViewState extends State<MainTabView> {
  int _selectedIndex = 0;
  final List<Widget> _screens = const [
    HomeScreen(),
    BrowseScreen(),
    SearchScreen(),
    DownloadsScreen(),
    SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: CupertinoTabBar(
        backgroundColor: const Color(0xFF0D0517).withOpacity(0.9),
        activeColor: Colors.white,
        inactiveColor: Colors.grey.shade600,
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        items: const [
          BottomNavigationBarItem(icon: Icon(CupertinoIcons.home), label: 'الرئيسية'),
          BottomNavigationBarItem(icon: Icon(CupertinoIcons.square_grid_2x2_fill), label: 'تصفح'),
          BottomNavigationBarItem(icon: Icon(CupertinoIcons.search), label: 'بحث'),
          BottomNavigationBarItem(icon: Icon(CupertinoIcons.arrow_down_circle_fill), label: 'التحميلات'),
          BottomNavigationBarItem(icon: Icon(CupertinoIcons.bars), label: 'المزيد'),
        ],
      ),
    );
  }
}
'''
with open(f"{BASE}/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(main_dart)

# 5. Models (كل الملفات)
models = {
    "video_item.dart": '''class VideoItem {
  final String id;
  final String title;
  final String imageUrl;
  final String type;
  VideoItem({required this.id, required this.title, required this.imageUrl, required this.type});
  Map<String, dynamic> toJson() => {'id': id, 'title': title, 'imageUrl': imageUrl, 'type': type};
  factory VideoItem.fromJson(Map<String, dynamic> json) => VideoItem(
        id: json['id'], title: json['title'], imageUrl: json['imageUrl'], type: json['type'],
      );
}
''',
    "episode.dart": '''class EpisodeItem {
  final String id;
  final String title;
  final String url;
  final String url1080;
  final String url360;
  final String subtitleUrl;
  final String subtitleVttUrl;
  EpisodeItem({
    required this.id, required this.title, required this.url, required this.url1080,
    required this.url360, required this.subtitleUrl, required this.subtitleVttUrl,
  });
  String get season {
    final lower = title.toLowerCase();
    if (lower.contains('s')) {
      final match = RegExp(r'(S\\d+|موسم \\d+)', caseSensitive: false).firstMatch(title);
      if (match != null) {
        final num = match.group(0)!.replaceAll(RegExp(r'[^0-9]'), '');
        return 'الموسم ' + num;
      }
    }
    return 'الموسم 1';
  }
}
''',
    "media_details.dart": '''import 'episode.dart';
class MediaDetails {
  String title; String imageUrl; String year; String genre; String rating;
  String runtime; String synopsis; bool isMovie; String movieUrl;
  String movieUrl1080; String movieUrl360; String movieSubtitleUrl;
  String movieSubtitleVttUrl; List<EpisodeItem> episodes;
  MediaDetails({
    this.title = '', this.imageUrl = '', this.year = '', this.genre = '',
    this.rating = '', this.runtime = '', this.synopsis = '', this.isMovie = true,
    this.movieUrl = '', this.movieUrl1080 = '', this.movieUrl360 = '',
    this.movieSubtitleUrl = '', this.movieSubtitleVttUrl = '', this.episodes = const [],
  });
  Map<String, List<EpisodeItem>> get seasonsDict {
    final map = <String, List<EpisodeItem>>{};
    for (var ep in episodes) {
      final s = ep.season;
      map.putIfAbsent(s, () => []).add(ep);
    }
    return map;
  }
  List<String> get sortedSeasons {
    final keys = seasonsDict.keys.toList();
    keys.sort((a, b) {
      final n1 = int.tryParse(a.replaceAll(RegExp(r'[^0-9]'), '')) ?? 0;
      final n2 = int.tryParse(b.replaceAll(RegExp(r'[^0-9]'), '')) ?? 0;
      return n1.compareTo(n2);
    });
    return keys;
  }
}
''',
    "watch_progress.dart": '''class WatchProgress {
  final String itemId; final String title; final String imageUrl;
  final String episodeId; final String episodeTitle; final double progressSeconds;
  final double durationSeconds; final DateTime updatedAt; final String videoUrl;
  final String videoUrl1080; final String videoUrl360; final String subtitleUrl;
  final String subtitleVttUrl;
  WatchProgress({
    required this.itemId, required this.title, required this.imageUrl,
    required this.episodeId, required this.episodeTitle, required this.progressSeconds,
    required this.durationSeconds, required this.updatedAt, required this.videoUrl,
    required this.videoUrl1080, required this.videoUrl360, required this.subtitleUrl,
    required this.subtitleVttUrl,
  });
  Map<String, dynamic> toJson() => {
        'itemId': itemId, 'title': title, 'imageUrl': imageUrl, 'episodeId': episodeId,
        'episodeTitle': episodeTitle, 'progressSeconds': progressSeconds,
        'durationSeconds': durationSeconds, 'updatedAt': updatedAt.toIso8601String(),
        'videoUrl': videoUrl, 'videoUrl1080': videoUrl1080, 'videoUrl360': videoUrl360,
        'subtitleUrl': subtitleUrl, 'subtitleVttUrl': subtitleVttUrl,
      };
  factory WatchProgress.fromJson(Map<String, dynamic> json) => WatchProgress(
        itemId: json['itemId'], title: json['title'], imageUrl: json['imageUrl'],
        episodeId: json['episodeId'], episodeTitle: json['episodeTitle'],
        progressSeconds: (json['progressSeconds'] as num).toDouble(),
        durationSeconds: (json['durationSeconds'] as num).toDouble(),
        updatedAt: DateTime.parse(json['updatedAt']), videoUrl: json['videoUrl'],
        videoUrl1080: json['videoUrl1080'], videoUrl360: json['videoUrl360'],
        subtitleUrl: json['subtitleUrl'], subtitleVttUrl: json['subtitleVttUrl'],
      );
}
''',
    "download_task.dart": '''class DownloadTaskItem {
  final String id; final String title; final String imageUrl; final bool isMovie;
  final String videoUrl; final String subtitleUrl; double progress;
  bool isCompleted; String? localVideoPath;
  DownloadTaskItem({
    required this.id, required this.title, required this.imageUrl, required this.isMovie,
    required this.videoUrl, required this.subtitleUrl, this.progress = 0.0,
    this.isCompleted = false, this.localVideoPath,
  });
  Map<String, dynamic> toJson() => {
        'id': id, 'title': title, 'imageUrl': imageUrl, 'isMovie': isMovie,
        'videoUrl': videoUrl, 'subtitleUrl': subtitleUrl, 'progress': progress,
        'isCompleted': isCompleted, 'localVideoPath': localVideoPath,
      };
  factory DownloadTaskItem.fromJson(Map<String, dynamic> json) => DownloadTaskItem(
        id: json['id'], title: json['title'], imageUrl: json['imageUrl'],
        isMovie: json['isMovie'], videoUrl: json['videoUrl'], subtitleUrl: json['subtitleUrl'],
        progress: (json['progress'] as num).toDouble(),
        isCompleted: json['isCompleted'], localVideoPath: json['localVideoPath'],
      );
}
''',
    "site_category.dart": '''class SiteCategory {
  final int id; final String nameAr; final String nameEn;
  const SiteCategory({required this.id, required this.nameAr, required this.nameEn});
}
const List<SiteCategory> SITE_CATEGORIES = [
  SiteCategory(id: 0, nameAr: 'أفلام إنجليزية', nameEn: 'English Movies'),
  SiteCategory(id: 1, nameAr: 'مسلسلات أجنبية', nameEn: 'TV Series'),
  SiteCategory(id: 2, nameAr: 'أنمي', nameEn: 'Anime Series'),
  SiteCategory(id: 3, nameAr: 'بوليوود', nameEn: 'Bollywood Movies'),
  SiteCategory(id: 4, nameAr: 'مسلسلات عربية', nameEn: 'Arabic Series'),
  SiteCategory(id: 5, nameAr: 'مسلسلات آسيوية', nameEn: 'Asian Series'),
  SiteCategory(id: 6, nameAr: 'أفلام آسيوية', nameEn: 'Asian Movies'),
  SiteCategory(id: 7, nameAr: 'أفلام عربية', nameEn: 'Arabic Movies'),
  SiteCategory(id: 8, nameAr: 'مسلسلات بوليوود', nameEn: 'Bollywood Series'),
  SiteCategory(id: 9, nameAr: 'أفلام أنمي', nameEn: 'Anime Movies'),
  SiteCategory(id: 10, nameAr: 'أفلام مكتب الصندوق', nameEn: 'US Box Office'),
  SiteCategory(id: 13, nameAr: 'سينما عربية', nameEn: 'Arabic Cinemas'),
  SiteCategory(id: 14, nameAr: 'أفلام تركية', nameEn: 'Turkish Movies'),
  SiteCategory(id: 15, nameAr: 'مسلسلات تركية', nameEn: 'Turkish Series'),
  SiteCategory(id: 16, nameAr: 'أفلام كرتون', nameEn: 'Cartoon Movies'),
  SiteCategory(id: 17, nameAr: 'مسلسلات كرتون', nameEn: 'Cartoon Series'),
  SiteCategory(id: 18, nameAr: 'أفلام أجنبية', nameEn: 'Foreign Movies'),
  SiteCategory(id: 20, nameAr: 'مسلسلات مدبلجة عربي', nameEn: 'Arabic Dubbed Series'),
  SiteCategory(id: 21, nameAr: 'أفلام مدبلجة عربي', nameEn: 'Arabic Dubbed Movies'),
  SiteCategory(id: 1014, nameAr: 'أفلام كردية', nameEn: 'Kurdish Movies'),
  SiteCategory(id: 1015, nameAr: 'مسلسلات كردية', nameEn: 'Kurdish Series'),
  SiteCategory(id: 1022, nameAr: 'أنمي عربي', nameEn: 'Arabic Anime'),
  SiteCategory(id: 1029, nameAr: 'أنمي مدبلج إنجليزي', nameEn: 'English Dubbed Anime'),
];
'''
}
for fname, content in models.items():
    with open(f"{BASE}/lib/models/{fname}", "w", encoding="utf-8") as f:
        f.write(content)

# 6. Services

# ✅ FIX الرئيسي: scraper.dart
# المشاكل المُصلحة:
# 1. baseUrl بدون / في النهاية → منع double-slash في الـ URLs
# 2. إضافة Referer و Cookie و Accept-Language headers
# 3. زيادة timeout إلى 30 ثانية
# 4. إضافة retry تلقائي (3 محاولات) عند الفشل
# 5. استخدام IOClient مع HttpClient مُعدّل يتجاوز SSL
# 6. إضافة followRedirects صريح
scraper_dart = '''import 'dart:async';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http/io_client.dart';
import '../models/video_item.dart';
import '../models/episode.dart';
import '../models/media_details.dart';

class MovieScraper {
  // ✅ FIX: بدون / في النهاية لمنع double-slash
  static const String baseUrl = 'https://movie.vodu.me';

  static const String _userAgent =
      'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36';

  // ✅ FIX: IOClient يتجاوز SSL بشكل موثوق على Android
  http.Client _buildClient() {
    final httpClient = HttpClient()
      ..badCertificateCallback =
          (X509Certificate cert, String host, int port) => true
      ..connectionTimeout = const Duration(seconds: 30);
    return IOClient(httpClient);
  }

  // ✅ FIX: headers شاملة + Referer + retry تلقائي
  Future<http.Response> _getWithHeaders(String url, {int retries = 3}) async {
    final headers = {
      'User-Agent': _userAgent,
      'Accept':
          'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
      'Accept-Encoding': 'gzip, deflate',
      'Referer': baseUrl + '/',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1',
    };

    for (int attempt = 1; attempt <= retries; attempt++) {
      final client = _buildClient();
      try {
        final response = await client
            .get(Uri.parse(url), headers: headers)
            .timeout(const Duration(seconds: 30));
        client.close();
        if (response.statusCode == 200) return response;
        if (attempt == retries) return response;
      } on TimeoutException {
        client.close();
        if (attempt == retries) rethrow;
        await Future.delayed(Duration(seconds: attempt * 2));
      } on SocketException {
        client.close();
        if (attempt == retries) rethrow;
        await Future.delayed(Duration(seconds: attempt * 2));
      } catch (e) {
        client.close();
        if (attempt == retries) rethrow;
        await Future.delayed(Duration(seconds: attempt));
      }
    }
    throw Exception('فشل الاتصال بعد $retries محاولات');
  }

  Future<({List<VideoItem> hero, List<Map<String, dynamic>> categories})>
      fetchHome() async {
    try {
      // ✅ FIX: URL صحيح بدون double-slash
      final response = await _getWithHeaders('$baseUrl/index.php');
      if (response.statusCode != 200) {
        throw Exception('HTTP \${response.statusCode}');
      }
      final html = response.body;
      List<VideoItem> hero = [];
      List<Map<String, dynamic>> categoryList = [];

      final carReg = RegExp(
          r'<a href="index\\.php\\?do=view&type=post&id=(\\d+)"><img src="([^"]+)"[^>]*alt="([^"]*)"');
      for (final match in carReg.allMatches(html)) {
        final id = match.group(1)!;
        var img = match.group(2)!;
        final title = match.group(3)!;
        if (!img.startsWith('http')) img = '$baseUrl/$img';
        hero.add(VideoItem(id: id, title: title, imageUrl: img, type: 'post'));
      }

      final sectionReg = RegExp(
          r'<h3[^>]*>\\s*([^<]+)\\s*</h3>.*?<div class="homeseries">(.*?)</div>\\s*</div>',
          dotAll: true);
      for (final match in sectionReg.allMatches(html)) {
        final secTitle = match.group(1)!.trim();
        final body = match.group(2)!;
        final items = _parseItemXBlock(body);
        if (items.isNotEmpty) {
          categoryList.add({'name': secTitle, 'items': items});
        }
      }

      if (categoryList.isEmpty && hero.isNotEmpty) {
        categoryList
            .add({'name': 'الرائج الآن', 'items': hero.take(10).toList()});
      }
      return (hero: hero, categories: categoryList);
    } catch (e) {
      print('Scraper Error Home: $e');
      return (
        hero: <VideoItem>[],
        categories: <Map<String, dynamic>>[]
      );
    }
  }

  Future<List<VideoItem>> fetchCategory(int typeId, int page) async {
    try {
      // ✅ FIX: URL بدون double-slash
      final url = '$baseUrl/index.php?do=list&type=$typeId&page=$page';
      final response = await _getWithHeaders(url);
      if (response.statusCode != 200) return [];
      return _parseListPage(response.body);
    } catch (e) {
      return [];
    }
  }

  Future<List<VideoItem>> search(String query) async {
    try {
      final encoded = Uri.encodeComponent(query);
      final url = '$baseUrl/index.php?do=list&title=$encoded';
      final response = await _getWithHeaders(url);
      if (response.statusCode != 200) return [];
      return _parseListPage(response.body);
    } catch (e) {
      return [];
    }
  }

  Future<MediaDetails> fetchDetails(String id) async {
    try {
      final url = '$baseUrl/index.php?do=view&type=post&id=$id';
      final response = await _getWithHeaders(url);
      if (response.statusCode != 200) return MediaDetails();
      return _parseDetails(response.body);
    } catch (e) {
      return MediaDetails(title: 'حدث خطأ في جلب البيانات');
    }
  }

  List<VideoItem> _parseListPage(String html) {
    final List<VideoItem> items = [];
    final pattern = RegExp(
        r'href="index\\.php\\?do=view&type=post&id=(\\d+)"><img src="([^"]+)"[^>]*>\\s*</a>\\s*<div class="mytitle">\\s*<a[^>]*>([^<]+)</a>');
    for (final match in pattern.allMatches(html)) {
      final id = match.group(1)!;
      var img = match.group(2)!;
      final title = match.group(3)!.trim();
      if (!img.startsWith('http')) img = '$baseUrl/$img';
      items.add(VideoItem(id: id, title: title, imageUrl: img, type: 'post'));
    }
    return items;
  }

  List<VideoItem> _parseItemXBlock(String html) {
    final List<VideoItem> items = [];
    final pattern = RegExp(
        r'<div class="itemx"[^>]*>.*?<img src="([^"]+)".*?<div class="mytitle">([^<]+)</div>',
        dotAll: true);
    int idx = 1;
    for (final match in pattern.allMatches(html)) {
      var img = match.group(1)!;
      final title = match.group(2)!.trim();
      if (!img.startsWith('http')) img = '$baseUrl/$img';
      items.add(VideoItem(
          id: 'home_${idx}_${title.substring(0, title.length > 10 ? 10 : title.length)}',
          title: title,
          imageUrl: img,
          type: 'post'));
      idx++;
    }
    return items;
  }

  MediaDetails _parseDetails(String html) {
    MediaDetails d = MediaDetails();
    final titleMatch = RegExp(r'<h1>(.*?)</h1>').firstMatch(html);
    if (titleMatch != null) d.title = titleMatch.group(1)!;
    final yearMatch =
        RegExp(r'<span>Year:\\s*</span>\\s*([^<]+)').firstMatch(html);
    if (yearMatch != null) d.year = yearMatch.group(1)!.trim();
    final genreMatch =
        RegExp(r'<span>Genre:\\s*</span>\\s*([^<]+)').firstMatch(html);
    if (genreMatch != null) d.genre = genreMatch.group(1)!.trim();
    final ratingMatch =
        RegExp(r'<span>IMdB Rating:\\s*</span>\\s*([^<]+)').firstMatch(html);
    if (ratingMatch != null) d.rating = ratingMatch.group(1)!.trim();
    final runtimeMatch =
        RegExp(r'<span>Runtime:\\s*</span>\\s*([^<]+)').firstMatch(html);
    if (runtimeMatch != null) d.runtime = runtimeMatch.group(1)!.trim();
    final synopsisMatch =
        RegExp(r'<h3>Synopsis:</h3>.*?<h4>(.*?)</h4>', dotAll: true)
            .firstMatch(html);
    if (synopsisMatch != null) d.synopsis = synopsisMatch.group(1)!.trim();
    final imgMatch =
        RegExp(r'<img src="([^"]+)" class="img-responsive"').firstMatch(html);
    if (imgMatch != null) {
      var img = imgMatch.group(1)!;
      if (!img.startsWith('http')) img = '$baseUrl/$img';
      d.imageUrl = img;
    }
    final epBlock =
        RegExp(r'<li class="episodeitem">(.*?)</li>', dotAll: true);
    final episodes = <EpisodeItem>[];
    for (final match in epBlock.allMatches(html)) {
      final block = match.group(1)!;
      final id = RegExp(r'data-id="(\\d+)"').firstMatch(block)?.group(1) ?? '';
      if (id.isEmpty) continue;
      final title =
          RegExp(r'data-title="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final url =
          RegExp(r'data-url="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final url360 =
          RegExp(r'data-url360="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final url1080 =
          RegExp(r'data-url1080="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final srt =
          RegExp(r'data-srt="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final vtt =
          RegExp(r'data-webvtt="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      if (url.isNotEmpty) {
        episodes.add(EpisodeItem(
          id: id,
          title: title.isEmpty ? 'الحلقة \${episodes.length + 1}' : title,
          url: url,
          url1080: url1080,
          url360: url360,
          subtitleUrl: srt,
          subtitleVttUrl: vtt,
        ));
      }
    }
    if (episodes.isNotEmpty) {
      d.isMovie = false;
      d.episodes = episodes;
    } else {
      final movieMatch = RegExp(
              r'data-url="([^"]+)"[^>]*data-url360="([^"]*)"[^>]*data-url1080="([^"]*)"[^>]*data-srt="([^"]*)"[^>]*data-webvtt="([^"]*)"')
          .firstMatch(html);
      if (movieMatch != null) {
        d.movieUrl = movieMatch.group(1)!;
        d.movieUrl360 = movieMatch.group(2)!;
        d.movieUrl1080 = movieMatch.group(3)!;
        d.movieSubtitleUrl = movieMatch.group(4)!;
        d.movieSubtitleVttUrl = movieMatch.group(5)!;
      }
    }
    return d;
  }
}
'''
with open(f"{BASE}/lib/services/scraper.dart", "w", encoding="utf-8") as f:
    f.write(scraper_dart)

services_extra = {
    "subtitle_parser.dart": '''import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http/io_client.dart';

class SubtitleCue {
  final double startTime; final double endTime; final String text;
  SubtitleCue({required this.startTime, required this.endTime, required this.text});
}

class SubtitleParser {
  static http.Client _buildClient() {
    final httpClient = HttpClient()
      ..badCertificateCallback =
          (X509Certificate cert, String host, int port) => true
      ..connectionTimeout = const Duration(seconds: 20);
    return IOClient(httpClient);
  }

  static Future<List<SubtitleCue>> parse(String url) async {
    if (url.isEmpty) return [];
    String clean = url;
    if (!clean.startsWith('http')) clean = 'https://movie.vodu.me/' + clean;
    final client = _buildClient();
    try {
      final response = await client
          .get(Uri.parse(clean), headers: {
            'User-Agent':
                'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
            'Referer': 'https://movie.vodu.me/',
          })
          .timeout(const Duration(seconds: 15));
      client.close();
      if (response.statusCode != 200) return [];
      final String content = response.body;
      if (content.contains('WEBVTT')) return _parseWebVTT(content);
      return _parseSRT(content);
    } catch (e) {
      client.close();
      return [];
    }
  }

  static List<SubtitleCue> _parseSRT(String content) {
    final List<SubtitleCue> cues = [];
    final blocks = content.split('\\n\\n');
    for (final block in blocks) {
      final lines = block.split('\\n').map((l) => l.trim()).where((l) => l.isNotEmpty).toList();
      if (lines.length < 3) continue;
      final timeLine = lines[1]; final textLines = lines.sublist(2);
      final text = textLines.join('\\n').replaceAll(RegExp(r'<[^>]+>'), '').trim();
      if (text.isEmpty) continue;
      final times = timeLine.split(' --> ');
      if (times.length != 2) continue;
      final start = _parseSRTTime(times[0]); final end = _parseSRTTime(times[1]);
      if (start != null && end != null) cues.add(SubtitleCue(startTime: start, endTime: end, text: text));
    }
    return cues;
  }

  static double? _parseSRTTime(String timeStr) {
    final clean = timeStr.trim(); final parts = clean.split(',');
    if (parts.length != 2) return null;
    final ms = double.tryParse(parts[1]); if (ms == null) return null;
    final comps = parts[0].split(':'); if (comps.length != 3) return null;
    final h = double.tryParse(comps[0]) ?? 0;
    final m = double.tryParse(comps[1]) ?? 0;
    final s = double.tryParse(comps[2]) ?? 0;
    return h * 3600 + m * 60 + s + ms / 1000;
  }

  static List<SubtitleCue> _parseWebVTT(String content) {
    final List<SubtitleCue> cues = [];
    final lines = content.split('\\n');
    int i = 0;
    while (i < lines.length) {
      final line = lines[i].trim();
      if (line.contains('-->')) {
        final times = line.split('-->');
        if (times.length != 2) { i++; continue; }
        final start = _parseVTTTime(times[0]); final end = _parseVTTTime(times[1]);
        if (start != null && end != null) {
          final textLines = <String>[]; i++;
          while (i < lines.length && lines[i].trim().isNotEmpty) {
            textLines.add(lines[i].trim()); i++;
          }
          final text = textLines.join('\\n').replaceAll(RegExp(r'<[^>]+>'), '').trim();
          if (text.isNotEmpty) cues.add(SubtitleCue(startTime: start, endTime: end, text: text));
        }
      }
      i++;
    }
    return cues;
  }

  static double? _parseVTTTime(String timeStr) {
    final clean = timeStr.trim(); final parts = clean.split(':');
    double h = 0, m = 0, s = 0;
    if (parts.length == 3) {
      h = double.tryParse(parts[0]) ?? 0;
      m = double.tryParse(parts[1]) ?? 0;
      final secParts = parts[2].split('.');
      s = double.tryParse(secParts[0]) ?? 0;
      if (secParts.length == 2) s += (double.tryParse(secParts[1]) ?? 0) / 1000;
    } else if (parts.length == 2) {
      m = double.tryParse(parts[0]) ?? 0;
      final secParts = parts[1].split('.');
      s = double.tryParse(secParts[0]) ?? 0;
      if (secParts.length == 2) s += (double.tryParse(secParts[1]) ?? 0) / 1000;
    } else return null;
    return h * 3600 + m * 60 + s;
  }
}
''',
    "progress_store.dart": '''import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/watch_progress.dart';
class WatchProgressStore {
  static final WatchProgressStore _instance = WatchProgressStore._internal();
  factory WatchProgressStore() => _instance;
  WatchProgressStore._internal();
  static const String _key = 'UTanWatchProgress_v3';
  Map<String, WatchProgress> _allProgress = {};
  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final String? data = prefs.getString(_key);
    if (data != null) {
      final Map<String, dynamic> decoded = Map.from(jsonDecode(data));
      _allProgress = decoded.map((k, v) => MapEntry(k, WatchProgress.fromJson(v)));
    }
  }
  Future<void> save({
    required String itemId, required String title, required String imageUrl,
    required String episodeId, required String episodeTitle, required double progress,
    required double duration, required String videoUrl, required String videoUrl1080,
    required String videoUrl360, required String subUrl, required String subVttUrl,
  }) async {
    _allProgress[itemId] = WatchProgress(
      itemId: itemId, title: title, imageUrl: imageUrl, episodeId: episodeId,
      episodeTitle: episodeTitle, progressSeconds: progress, durationSeconds: duration,
      updatedAt: DateTime.now(), videoUrl: videoUrl, videoUrl1080: videoUrl1080,
      videoUrl360: videoUrl360, subtitleUrl: subUrl, subtitleVttUrl: subVttUrl,
    );
    await _persist();
  }
  Future<void> remove(String itemId) async { _allProgress.remove(itemId); await _persist(); }
  Future<void> clearAll() async { _allProgress.clear(); await _persist(); }
  WatchProgress? progress(String itemId) => _allProgress[itemId];
  List<WatchProgress> get recent => _allProgress.values.toList()..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, jsonEncode(_allProgress.map((k, v) => MapEntry(k, v.toJson()))));
  }
}
''',
    "download_manager.dart": '''import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:gallery_saver/gallery_saver.dart';
import 'package:permission_handler/permission_handler.dart';
import '../models/download_task.dart';

class DownloadManager {
  static final DownloadManager _instance = DownloadManager._internal();
  factory DownloadManager() => _instance;
  DownloadManager._internal();
  static const String _key = 'UTanDownloads_v1';
  List<DownloadTaskItem> _activeDownloads = [];
  late final Dio _dio;
  List<DownloadTaskItem> get activeDownloads => List.unmodifiable(_activeDownloads);

  Future<void> init() async {
    // ✅ FIX: Dio مُعدّ لتجاوز SSL أيضاً
    _dio = Dio(BaseOptions(
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 0),
      headers: {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
        'Referer': 'https://movie.vodu.me/',
      },
    ));
    (_dio.httpClientAdapter as dynamic).onHttpClientCreate =
        (HttpClient client) {
      client.badCertificateCallback =
          (X509Certificate cert, String host, int port) => true;
      return client;
    };
    final prefs = await SharedPreferences.getInstance();
    final String? data = prefs.getString(_key);
    if (data != null) {
      final List<dynamic> list = jsonDecode(data);
      _activeDownloads = list.map((e) => DownloadTaskItem.fromJson(e)).toList();
    }
  }

  Future<void> startDownload({
    required String id, required String title, required String imageUrl,
    required bool isMovie, required String videoUrl, required String subtitleUrl,
  }) async {
    if (_activeDownloads.any((d) => d.id == id)) return;
    final task = DownloadTaskItem(id: id, title: title, imageUrl: imageUrl, isMovie: isMovie, videoUrl: videoUrl, subtitleUrl: subtitleUrl);
    _activeDownloads.add(task); await _persist();
    await Permission.storage.request();
    try {
      final dir = await getTemporaryDirectory();
      final savePath = '\${dir.path}/$id.mp4';
      await _dio.download(videoUrl, savePath, onReceiveProgress: (received, total) {
        if (total <= 0) return;
        final index = _activeDownloads.indexWhere((d) => d.id == id);
        if (index != -1) { _activeDownloads[index].progress = received / total; _persist(); }
      });
      final idx = _activeDownloads.indexWhere((d) => d.id == id);
      if (idx != -1) {
        _activeDownloads[idx].isCompleted = true;
        _activeDownloads[idx].localVideoPath = savePath;
        await _persist();
        await GallerySaver.saveVideo(savePath, toDcim: true);
      }
    } catch (e) {
      cancel(id);
    }
  }

  Future<void> cancel(String id) async { _activeDownloads.removeWhere((d) => d.id == id); await _persist(); }

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, jsonEncode(_activeDownloads.map((e) => e.toJson()).toList()));
  }
}
''',
    "favorites_store.dart": '''import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/video_item.dart';
class FavoritesStore {
  static final FavoritesStore _instance = FavoritesStore._internal();
  factory FavoritesStore() => _instance;
  FavoritesStore._internal();
  static const String _key = 'UTanFavorites_v1';
  List<VideoItem> _items = [];
  List<VideoItem> get items => List.unmodifiable(_items);
  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final String? data = prefs.getString(_key);
    if (data != null) {
      final List<dynamic> list = jsonDecode(data);
      _items = list.map((e) => VideoItem.fromJson(e)).toList();
    }
  }
  Future<void> toggle(VideoItem item) async {
    final index = _items.indexWhere((i) => i.id == item.id);
    if (index != -1) _items.removeAt(index);
    else _items.insert(0, item);
    await _persist();
  }
  bool isFavorite(String id) => _items.any((i) => i.id == id);
  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, jsonEncode(_items.map((e) => e.toJson()).toList()));
  }
}
''',
    "settings_store.dart": '''import 'package:shared_preferences/shared_preferences.dart';
class SettingsStore {
  static final SettingsStore _instance = SettingsStore._internal();
  factory SettingsStore() => _instance;
  SettingsStore._internal();
  double subtitleFontSize = 22.0; String subtitleColorHex = '#FFFFFF';
  double subtitleBgOpacity = 0.6; double subtitleBottomPad = 60.0; bool subtitlesEnabled = true;
  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    subtitleFontSize = prefs.getDouble('sub_fontSize') ?? 22.0;
    subtitleColorHex = prefs.getString('sub_colorHex') ?? '#FFFFFF';
    subtitleBgOpacity = prefs.getDouble('sub_bgOpacity') ?? 0.6;
    subtitleBottomPad = prefs.getDouble('sub_bottomPad') ?? 60.0;
    subtitlesEnabled = prefs.getBool('sub_enabled') ?? true;
  }
  Future<void> save() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('sub_fontSize', subtitleFontSize);
    await prefs.setString('sub_colorHex', subtitleColorHex);
    await prefs.setDouble('sub_bgOpacity', subtitleBgOpacity);
    await prefs.setDouble('sub_bottomPad', subtitleBottomPad);
    await prefs.setBool('sub_enabled', subtitlesEnabled);
  }
}
'''
}
for fname, content in services_extra.items():
    with open(f"{BASE}/lib/services/{fname}", "w", encoding="utf-8") as f:
        f.write(content)

# 7. Widgets
widgets = {
    "poster_card.dart": '''import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/watch_progress.dart';
import '../models/video_item.dart';

class PosterCard extends StatelessWidget {
  final VideoItem item;
  final WatchProgress? progress;
  const PosterCard({super.key, required this.item, this.progress});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 110,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Stack(
            children: [
              Container(
                width: 110, height: 160,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(12),
                  color: const Color(0xFF1C1C24),
                ),
                clipBehavior: Clip.antiAlias,
                child: CachedNetworkImage(
                  imageUrl: item.imageUrl, fit: BoxFit.cover,
                  errorWidget: (_, __, ___) => Container(color: const Color(0xFF1C1C24)),
                ),
              ),
              Positioned.fill(
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    gradient: const LinearGradient(
                      begin: Alignment.topCenter, end: Alignment.bottomCenter,
                      colors: [Colors.transparent, Colors.black54],
                    ),
                  ),
                ),
              ),
              if (progress != null && progress!.durationSeconds > 0)
                Positioned(
                  bottom: 0, left: 0, right: 0,
                  child: LinearProgressIndicator(
                    value: progress!.progressSeconds / progress!.durationSeconds,
                    backgroundColor: Colors.white30,
                    valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFFE50914)),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 6),
          Text(item.title,
              style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white),
              maxLines: 2, overflow: TextOverflow.ellipsis),
        ],
      ),
    );
  }
}
''',
    "hero_banner.dart": '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/video_item.dart';
import '../screens/details_screen.dart';
import '../services/favorites_store.dart';

class HeroBanner extends StatefulWidget {
  final List<VideoItem> items;
  const HeroBanner({super.key, required this.items});
  @override
  State<HeroBanner> createState() => _HeroBannerState();
}

class _HeroBannerState extends State<HeroBanner> {
  late PageController _controller;
  int _current = 0;

  @override
  void initState() {
    super.initState();
    _controller = PageController();
    Future.delayed(const Duration(seconds: 5), _autoPlay);
  }

  void _autoPlay() {
    if (_controller.hasClients && widget.items.length > 1 && mounted) {
      _controller.nextPage(duration: const Duration(milliseconds: 800), curve: Curves.easeInOut);
      Future.delayed(const Duration(seconds: 5), _autoPlay);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (widget.items.isEmpty) return const SizedBox.shrink();
    return SizedBox(
      height: 500,
      child: PageView.builder(
        controller: _controller,
        onPageChanged: (i) => setState(() => _current = i),
        itemCount: widget.items.length > 8 ? 8 : widget.items.length,
        itemBuilder: (context, i) {
          final item = widget.items[i];
          return Stack(
            fit: StackFit.expand,
            children: [
              CachedNetworkImage(imageUrl: item.imageUrl, fit: BoxFit.cover),
              Container(
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter, end: Alignment.bottomCenter,
                    colors: [Colors.transparent, Colors.transparent, Color(0x990D0517), Color(0xFF0D0517)],
                    stops: [0.0, 0.5, 0.8, 1.0],
                  ),
                ),
              ),
              Positioned(
                bottom: 40, left: 20, right: 20,
                child: Column(
                  children: [
                    Text(item.title,
                        style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 0.5),
                        textAlign: TextAlign.center),
                    const SizedBox(height: 15),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        GestureDetector(
                          onTap: () => Navigator.push(context, CupertinoPageRoute(builder: (_) => DetailsScreen(itemId: item.id))),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(8)),
                            child: const Row(children: [Icon(CupertinoIcons.play_arrow_solid, color: Colors.black, size: 20), SizedBox(width: 8), Text('Play', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 16))]),
                          ),
                        ),
                        const SizedBox(width: 15),
                        GestureDetector(
                          onTap: () async { await FavoritesStore().toggle(item); setState(() {}); },
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                            decoration: BoxDecoration(color: const Color(0xFF2C2C34), borderRadius: BorderRadius.circular(8)),
                            child: Row(children: [Icon(FavoritesStore().isFavorite(item.id) ? CupertinoIcons.checkmark_alt : CupertinoIcons.add, color: Colors.white, size: 20), const SizedBox(width: 8), const Text('My List', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16))]),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
''',
    "continue_row.dart": '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../services/progress_store.dart';
import '../screens/player_screen.dart';

class ContinueWatchingRow extends StatelessWidget {
  const ContinueWatchingRow({super.key});

  @override
  Widget build(BuildContext context) {
    final recent = WatchProgressStore().recent;
    if (recent.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: Text('متابعة المشاهدة', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
        ),
        SizedBox(
          height: 120,
          child: ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 15),
            scrollDirection: Axis.horizontal,
            itemCount: recent.length,
            itemBuilder: (context, i) {
              final p = recent[i];
              return GestureDetector(
                onTap: () => Navigator.push(context, CupertinoPageRoute(builder: (_) => PlayerScreen(
                  itemId: p.itemId, itemTitle: p.title, itemImageUrl: p.imageUrl,
                  videoUrl: p.videoUrl, videoUrl1080: p.videoUrl1080, videoUrl360: p.videoUrl360,
                  subtitleUrl: p.subtitleUrl, subtitleVttUrl: p.subtitleVttUrl,
                  episodeId: p.episodeId, episodeTitle: p.episodeTitle, startAt: p.progressSeconds,
                ))),
                child: Container(
                  width: 160, margin: const EdgeInsets.symmetric(horizontal: 5),
                  child: Stack(
                    children: [
                      Container(
                        width: 160, height: 100,
                        decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), color: const Color(0xFF1C1C24)),
                        clipBehavior: Clip.antiAlias,
                        child: CachedNetworkImage(imageUrl: p.imageUrl, fit: BoxFit.cover),
                      ),
                      Positioned.fill(
                        child: Container(
                          decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), color: Colors.black38),
                          child: const Center(child: Icon(CupertinoIcons.play_circle_fill, size: 40, color: Colors.white)),
                        ),
                      ),
                      if (p.durationSeconds > 0)
                        Positioned(
                          bottom: 20, left: 0, right: 0,
                          child: LinearProgressIndicator(
                            value: p.progressSeconds / p.durationSeconds,
                            backgroundColor: Colors.white30,
                            valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFFE50914)),
                          ),
                        ),
                    ],
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
''',
    "category_row.dart": '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import '../models/video_item.dart';
import 'poster_card.dart';
import '../services/progress_store.dart';
import '../screens/details_screen.dart';

class CategoryRow extends StatelessWidget {
  final String title; final List<VideoItem> items;
  const CategoryRow({super.key, required this.title, required this.items});

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
        ),
        SizedBox(
          height: 160,
          child: ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 15),
            scrollDirection: Axis.horizontal,
            itemCount: items.length,
            itemBuilder: (context, i) {
              final item = items[i];
              return GestureDetector(
                onTap: () => Navigator.push(context, CupertinoPageRoute(builder: (_) => DetailsScreen(itemId: item.id))),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 5),
                  child: PosterCard(item: item, progress: WatchProgressStore().progress(item.id)),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
'''
}
for fname, content in widgets.items():
    with open(f"{BASE}/lib/widgets/{fname}", "w", encoding="utf-8") as f:
        f.write(content)

# 8. Screens

home_screen = '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import '../models/video_item.dart';
import '../services/scraper.dart';
import '../widgets/hero_banner.dart';
import '../widgets/continue_row.dart';
import '../widgets/category_row.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final MovieScraper _scraper = MovieScraper();
  bool _loading = true; String _error = '';
  List<VideoItem> _heroItems = []; List<Map<String, dynamic>> _categories = [];

  @override
  void initState() { super.initState(); _loadData(); }

  Future<void> _loadData() async {
    setState(() { _loading = true; _error = ''; });
    try {
      final data = await _scraper.fetchHome();
      if (mounted) {
        setState(() {
          _heroItems = data.hero;
          _categories = data.categories;
          _loading = false;
          if (_heroItems.isEmpty && _categories.isEmpty) {
            _error = 'فشل الاتصال، الرجاء المحاولة مجددا';
          }
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() { _loading = false; _error = 'فشل الاتصال، الرجاء المحاولة مجددا'; });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        body: Center(child: CupertinoActivityIndicator(radius: 20)),
      );
    }
    if (_error.isNotEmpty) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(_error, style: const TextStyle(color: Colors.white)),
              const SizedBox(height: 10),
              CupertinoButton.filled(onPressed: _loadData, child: const Text('إعادة المحاولة')),
            ],
          ),
        ),
      );
    }
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      extendBodyBehindAppBar: true,
      body: SingleChildScrollView(
        padding: const EdgeInsets.only(bottom: 50),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            HeroBanner(items: _heroItems),
            Transform.translate(
              offset: const Offset(0, -30),
              child: const ContinueWatchingRow(),
            ),
            Transform.translate(
              offset: const Offset(0, -10),
              child: Column(
                children: _categories.map((cat) =>
                    CategoryRow(title: cat['name'], items: cat['items'])).toList(),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
'''
with open(f"{BASE}/lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(home_screen)

browse_screen = '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import '../models/site_category.dart';
import 'category_list_screen.dart';

class BrowseScreen extends StatelessWidget {
  const BrowseScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(title: const Text('تصفح', style: TextStyle(fontWeight: FontWeight.bold))),
      body: GridView.builder(
        padding: const EdgeInsets.all(15),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2, crossAxisSpacing: 15, mainAxisSpacing: 15, childAspectRatio: 1.2),
        itemCount: SITE_CATEGORIES.length,
        itemBuilder: (context, i) {
          final cat = SITE_CATEGORIES[i];
          return GestureDetector(
            onTap: () => Navigator.push(context, CupertinoPageRoute(builder: (_) => CategoryListScreen(category: cat))),
            child: Container(
              decoration: BoxDecoration(color: const Color(0xFF1C1C24), borderRadius: BorderRadius.circular(12)),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(CupertinoIcons.film, size: 40, color: Color(0xFFE50914)),
                  const SizedBox(height: 8),
                  Text(cat.nameAr, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
'''
with open(f"{BASE}/lib/screens/browse_screen.dart", "w", encoding="utf-8") as f:
    f.write(browse_screen)

category_list = '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import '../models/site_category.dart';
import '../models/video_item.dart';
import '../services/scraper.dart';
import '../widgets/poster_card.dart';
import 'details_screen.dart';

class CategoryListScreen extends StatefulWidget {
  final SiteCategory category;
  const CategoryListScreen({super.key, required this.category});
  @override
  State<CategoryListScreen> createState() => _CategoryListScreenState();
}

class _CategoryListScreenState extends State<CategoryListScreen> {
  final MovieScraper _scraper = MovieScraper();
  List<VideoItem> _items = []; int _page = 1; bool _loading = false; bool _hasMore = true;

  @override
  void initState() { super.initState(); _loadMore(); }

  Future<void> _loadMore() async {
    if (_loading || !_hasMore) return;
    setState(() => _loading = true);
    final newItems = await _scraper.fetchCategory(widget.category.id, _page);
    if (mounted) {
      setState(() {
        _items.addAll(newItems); _page++; _loading = false; _hasMore = newItems.isNotEmpty;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(title: Text(widget.category.nameAr)),
      body: GridView.builder(
        padding: const EdgeInsets.all(15),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 3, crossAxisSpacing: 10, mainAxisSpacing: 15, childAspectRatio: 0.66),
        itemCount: _items.length + (_hasMore ? 1 : 0),
        itemBuilder: (context, i) {
          if (i == _items.length) { _loadMore(); return const Center(child: CupertinoActivityIndicator()); }
          final item = _items[i];
          return GestureDetector(
              onTap: () => Navigator.push(context, CupertinoPageRoute(builder: (_) => DetailsScreen(itemId: item.id))),
              child: PosterCard(item: item));
        },
      ),
    );
  }
}
'''
with open(f"{BASE}/lib/screens/category_list_screen.dart", "w", encoding="utf-8") as f:
    f.write(category_list)

search_screen = '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import '../models/video_item.dart';
import '../services/scraper.dart';
import '../widgets/poster_card.dart';
import 'details_screen.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});
  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final MovieScraper _scraper = MovieScraper();
  final TextEditingController _controller = TextEditingController();
  List<VideoItem> _results = []; bool _loading = false;

  Future<void> _search() async {
    if (_controller.text.isEmpty) return;
    setState(() => _loading = true);
    final results = await _scraper.search(_controller.text);
    if (mounted) { setState(() { _results = results; _loading = false; }); }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(title: const Text('بحث')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(15),
            child: CupertinoSearchTextField(
              controller: _controller,
              style: const TextStyle(color: Colors.white),
              onSubmitted: (_) => _search(),
              backgroundColor: const Color(0xFF1C1C24),
            ),
          ),
          if (_loading) const Center(child: CupertinoActivityIndicator())
          else Expanded(
            child: GridView.builder(
              padding: const EdgeInsets.all(15),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3, crossAxisSpacing: 10, mainAxisSpacing: 15, childAspectRatio: 0.66),
              itemCount: _results.length,
              itemBuilder: (context, i) {
                final item = _results[i];
                return GestureDetector(
                    onTap: () => Navigator.push(context, CupertinoPageRoute(builder: (_) => DetailsScreen(itemId: item.id))),
                    child: PosterCard(item: item));
              },
            ),
          ),
        ],
      ),
    );
  }
}
'''
with open(f"{BASE}/lib/screens/search_screen.dart", "w", encoding="utf-8") as f:
    f.write(search_screen)

downloads_screen = '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../services/download_manager.dart';

class DownloadsScreen extends StatefulWidget {
  const DownloadsScreen({super.key});
  @override
  State<DownloadsScreen> createState() => _DownloadsScreenState();
}

class _DownloadsScreenState extends State<DownloadsScreen> {
  final DownloadManager _manager = DownloadManager();

  @override
  Widget build(BuildContext context) {
    final downloads = _manager.activeDownloads;
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(title: const Text('التحميلات')),
      body: downloads.isEmpty
          ? const Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
              Icon(CupertinoIcons.arrow_down_circle, size: 60, color: Colors.grey),
              SizedBox(height: 16),
              Text('لا توجد تحميلات', style: TextStyle(color: Colors.grey)),
            ]))
          : ListView.builder(
              itemCount: downloads.length,
              itemBuilder: (context, i) {
                final dl = downloads[i];
                return ListTile(
                  leading: ClipRRect(borderRadius: BorderRadius.circular(8), child: CachedNetworkImage(imageUrl: dl.imageUrl, width: 50, height: 70, fit: BoxFit.cover)),
                  title: Text(dl.title, style: const TextStyle(color: Colors.white)),
                  subtitle: dl.isCompleted
                      ? const Text('مكتمل - محفوظ في الصور', style: TextStyle(color: Colors.green))
                      : LinearProgressIndicator(value: dl.progress, backgroundColor: Colors.white30, valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFFE50914))),
                  trailing: IconButton(
                      icon: const Icon(CupertinoIcons.clear_circled, color: Colors.red),
                      onPressed: () { _manager.cancel(dl.id); setState(() {}); }),
                );
              },
            ),
    );
  }
}
'''
with open(f"{BASE}/lib/screens/downloads_screen.dart", "w", encoding="utf-8") as f:
    f.write(downloads_screen)

settings_screen = '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import '../services/settings_store.dart';
import '../services/progress_store.dart';
import 'history_screen.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});
  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final SettingsStore _settings = SettingsStore();
  final WatchProgressStore _progress = WatchProgressStore();
  bool _cacheCleared = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(title: const Text('المزيد')),
      body: ListView(
        children: [
          _buildSection('إعدادات الترجمة', [
            SwitchListTile(
              title: const Text('تفعيل الترجمة'),
              value: _settings.subtitlesEnabled,
              onChanged: (val) async { _settings.subtitlesEnabled = val; await _settings.save(); setState(() {}); },
              activeColor: const Color(0xFFE50914),
            ),
            if (_settings.subtitlesEnabled) ...[
              ListTile(
                title: const Text('حجم الخط'),
                subtitle: Slider(value: _settings.subtitleFontSize, min: 14, max: 40,
                    onChanged: (v) async { _settings.subtitleFontSize = v; await _settings.save(); setState(() {}); },
                    activeColor: const Color(0xFFE50914)),
              ),
              ListTile(
                title: const Text('الهامش السفلي'),
                subtitle: Slider(value: _settings.subtitleBottomPad, min: 20, max: 150,
                    onChanged: (v) async { _settings.subtitleBottomPad = v; await _settings.save(); setState(() {}); },
                    activeColor: const Color(0xFFE50914)),
              ),
              ListTile(
                title: const Text('شفافية الخلفية'),
                subtitle: Slider(value: _settings.subtitleBgOpacity, min: 0.0, max: 1.0,
                    onChanged: (v) async { _settings.subtitleBgOpacity = v; await _settings.save(); setState(() {}); },
                    activeColor: const Color(0xFFE50914)),
              ),
              const Padding(padding: EdgeInsets.all(16), child: Text('لون النص', style: TextStyle(fontWeight: FontWeight.bold))),
              SizedBox(
                height: 50,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: 4,
                  itemBuilder: (context, i) {
                    final colors = ['#FFFFFF', '#FFFF00', '#00FFFF', '#FF00FF'];
                    final hex = colors[i];
                    return GestureDetector(
                      onTap: () async { _settings.subtitleColorHex = hex; await _settings.save(); setState(() {}); },
                      child: Container(
                        margin: const EdgeInsets.symmetric(horizontal: 8), width: 40, height: 40,
                        decoration: BoxDecoration(
                          color: Color(int.parse(hex.substring(1), radix: 16) + 0xFF000000),
                          shape: BoxShape.circle,
                          border: Border.all(color: _settings.subtitleColorHex == hex ? Colors.white : Colors.transparent, width: 3),
                        ),
                      ),
                    );
                  },
                ),
              ),
            ],
          ]),
          _buildSection('البيانات', [
            ListTile(
              title: Text('سجل المشاهدة (\${_progress.recent.length})'),
              trailing: const Icon(CupertinoIcons.chevron_forward, color: Colors.grey),
              onTap: () => Navigator.push(context, CupertinoPageRoute(builder: (_) => const HistoryScreen())),
            ),
            ListTile(
              title: Text(_cacheCleared ? 'تم المسح!' : 'مسح التخزين المؤقت والسجل',
                  style: const TextStyle(color: Colors.red)),
              onTap: () async {
                await _progress.clearAll();
                setState(() => _cacheCleared = true);
                Future.delayed(const Duration(seconds: 2), () => setState(() => _cacheCleared = false));
              },
            ),
          ]),
        ],
      ),
    );
  }

  Widget _buildSection(String title, List<Widget> children) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.all(16), child: Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFFE50914)))),
      ...children,
      const Divider(color: Color(0xFF1C1C24)),
    ]);
  }
}
'''
with open(f"{BASE}/lib/screens/settings_screen.dart", "w", encoding="utf-8") as f:
    f.write(settings_screen)

history_screen = '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../services/progress_store.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});
  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  final WatchProgressStore _store = WatchProgressStore();

  @override
  Widget build(BuildContext context) {
    final items = _store.recent;
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(title: const Text('سجل المشاهدة')),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, i) {
          final p = items[i];
          return ListTile(
            leading: ClipRRect(borderRadius: BorderRadius.circular(8), child: CachedNetworkImage(imageUrl: p.imageUrl, width: 50, height: 70, fit: BoxFit.cover)),
            title: Text(p.title, style: const TextStyle(color: Colors.white)),
            subtitle: p.episodeTitle.isNotEmpty ? Text(p.episodeTitle, style: const TextStyle(color: Colors.grey)) : null,
            trailing: IconButton(
                icon: const Icon(CupertinoIcons.delete, color: Colors.red),
                onPressed: () async { await _store.remove(p.itemId); setState(() {}); }),
          );
        },
      ),
    );
  }
}
'''
with open(f"{BASE}/lib/screens/history_screen.dart", "w", encoding="utf-8") as f:
    f.write(history_screen)

details_screen = '''import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/video_item.dart';
import '../models/episode.dart';
import '../models/media_details.dart';
import '../services/scraper.dart';
import '../services/favorites_store.dart';
import '../services/download_manager.dart';
import 'player_screen.dart';

class DetailsScreen extends StatefulWidget {
  final String itemId;
  const DetailsScreen({super.key, required this.itemId});
  @override
  State<DetailsScreen> createState() => _DetailsScreenState();
}

class _DetailsScreenState extends State<DetailsScreen> {
  final MovieScraper _scraper = MovieScraper();
  MediaDetails? _details; bool _loading = true; String _selectedSeason = '';

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    final d = await _scraper.fetchDetails(widget.itemId);
    if (mounted) {
      setState(() {
        _details = d;
        _loading = false;
        if (d.sortedSeasons.isNotEmpty) _selectedSeason = d.sortedSeasons.first;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Scaffold(body: Center(child: CupertinoActivityIndicator()));
    final d = _details!;
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 350, pinned: true,
            backgroundColor: const Color(0xFF0D0517).withOpacity(0.9),
            flexibleSpace: FlexibleSpaceBar(
              background: Stack(
                fit: StackFit.expand,
                children: [
                  CachedNetworkImage(imageUrl: d.imageUrl, fit: BoxFit.cover),
                  Container(decoration: const BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter, end: Alignment.bottomCenter,
                      colors: [Colors.transparent, Color(0xFF0D0517)],
                      stops: [0.5, 1.0],
                    ),
                  )),
                ],
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(d.title, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 10),
                  Wrap(spacing: 8, children: [
                    if (d.year.isNotEmpty) _badge(d.year),
                    if (d.rating.isNotEmpty) _badge('⭐ \${d.rating}'),
                    if (d.runtime.isNotEmpty) _badge(d.runtime),
                  ]),
                  const SizedBox(height: 20),
                  Row(
                    children: [
                      Expanded(
                        child: CupertinoButton(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(8),
                          padding: EdgeInsets.zero,
                          onPressed: () => _play(d),
                          child: const Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                            Icon(CupertinoIcons.play_fill, color: Colors.black),
                            SizedBox(width: 8),
                            Text('شاهد الآن', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                          ]),
                        ),
                      ),
                      const SizedBox(width: 12),
                      IconButton(
                        onPressed: () => DownloadManager().startDownload(
                          id: widget.itemId, title: d.title, imageUrl: d.imageUrl, isMovie: d.isMovie,
                          videoUrl: d.isMovie ? d.movieUrl : (d.episodes.isNotEmpty ? d.episodes.first.url : ''),
                          subtitleUrl: d.isMovie ? d.movieSubtitleUrl : (d.episodes.isNotEmpty ? d.episodes.first.subtitleUrl : ''),
                        ),
                        icon: const Icon(CupertinoIcons.arrow_down_circle, color: Colors.white, size: 30),
                      ),
                      IconButton(
                        onPressed: () async {
                          await FavoritesStore().toggle(VideoItem(id: widget.itemId, title: d.title, imageUrl: d.imageUrl, type: 'post'));
                          setState(() {});
                        },
                        icon: Icon(FavoritesStore().isFavorite(widget.itemId) ? CupertinoIcons.checkmark_alt_circle_fill : CupertinoIcons.add_circled, color: Colors.white, size: 30),
                      ),
                    ],
                  ),
                  if (d.synopsis.isNotEmpty) ...[
                    const SizedBox(height: 20),
                    const Text('القصة', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Text(d.synopsis, style: TextStyle(color: Colors.grey.shade300, fontSize: 15, height: 1.5)),
                  ],
                  if (!d.isMovie && d.sortedSeasons.isNotEmpty) ...[
                    const SizedBox(height: 20),
                    SizedBox(
                      height: 40,
                      child: ListView.builder(
                        scrollDirection: Axis.horizontal,
                        itemCount: d.sortedSeasons.length,
                        itemBuilder: (context, i) {
                          final season = d.sortedSeasons[i];
                          return GestureDetector(
                            onTap: () => setState(() => _selectedSeason = season),
                            child: Container(
                              margin: const EdgeInsets.symmetric(horizontal: 5),
                              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                              decoration: BoxDecoration(
                                color: _selectedSeason == season ? const Color(0xFFE50914) : const Color(0xFF1C1C24),
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Text(season, style: TextStyle(fontWeight: FontWeight.bold, color: _selectedSeason == season ? Colors.white : Colors.grey)),
                            ),
                          );
                        },
                      ),
                    ),
                    const SizedBox(height: 16),
                    if (_selectedSeason.isNotEmpty && d.seasonsDict[_selectedSeason] != null)
                      ...d.seasonsDict[_selectedSeason]!.map((ep) => Container(
                        margin: const EdgeInsets.only(bottom: 10),
                        decoration: BoxDecoration(color: const Color(0xFF1C1C24), borderRadius: BorderRadius.circular(12)),
                        child: ListTile(
                          leading: const Icon(CupertinoIcons.play_circle_fill, color: Color(0xFFE50914), size: 30),
                          title: Text(ep.title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                          trailing: IconButton(
                            icon: const Icon(CupertinoIcons.arrow_down_circle, color: Colors.grey),
                            onPressed: () => DownloadManager().startDownload(id: ep.id, title: ep.title, imageUrl: d.imageUrl, isMovie: false, videoUrl: ep.url, subtitleUrl: ep.subtitleUrl),
                          ),
                          onTap: () => _playEpisode(ep, d),
                        ),
                      )),
                  ],
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _badge(String text) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
    decoration: BoxDecoration(color: Colors.white.withOpacity(0.15), borderRadius: BorderRadius.circular(6)),
    child: Text(text, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
  );

  void _play(MediaDetails d) {
    if (d.movieUrl.isEmpty && d.movieUrl1080.isEmpty && d.movieUrl360.isEmpty) return;
    Navigator.push(context, CupertinoPageRoute(builder: (_) => PlayerScreen(
      itemId: widget.itemId, itemTitle: d.title, itemImageUrl: d.imageUrl,
      videoUrl: d.movieUrl, videoUrl1080: d.movieUrl1080, videoUrl360: d.movieUrl360,
      subtitleUrl: d.movieSubtitleUrl, subtitleVttUrl: d.movieSubtitleVttUrl,
      episodeId: '', episodeTitle: '', startAt: 0,
    )));
  }

  void _playEpisode(EpisodeItem ep, MediaDetails d) {
    Navigator.push(context, CupertinoPageRoute(builder: (_) => PlayerScreen(
      itemId: widget.itemId, itemTitle: d.title, itemImageUrl: d.imageUrl,
      videoUrl: ep.url, videoUrl1080: ep.url1080, videoUrl360: ep.url360,
      subtitleUrl: ep.subtitleUrl, subtitleVttUrl: ep.subtitleVttUrl,
      episodeId: ep.id, episodeTitle: ep.title, startAt: 0,
    )));
  }
}
'''
with open(f"{BASE}/lib/screens/details_screen.dart", "w", encoding="utf-8") as f:
    f.write(details_screen)

player_screen = '''import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:video_player/video_player.dart';
import '../services/subtitle_parser.dart';
import '../services/settings_store.dart';
import '../services/progress_store.dart';

class PlayerScreen extends StatefulWidget {
  final String itemId, itemTitle, itemImageUrl;
  final String videoUrl, videoUrl1080, videoUrl360;
  final String subtitleUrl, subtitleVttUrl;
  final String episodeId, episodeTitle;
  final double startAt;

  const PlayerScreen({
    super.key,
    required this.itemId, required this.itemTitle, required this.itemImageUrl,
    required this.videoUrl, required this.videoUrl1080, required this.videoUrl360,
    required this.subtitleUrl, required this.subtitleVttUrl,
    required this.episodeId, required this.episodeTitle, required this.startAt,
  });

  @override
  State<PlayerScreen> createState() => _PlayerScreenState();
}

class _PlayerScreenState extends State<PlayerScreen> {
  VideoPlayerController? _controller;
  bool _isPlaying = true; bool _showControls = true; Timer? _hideTimer;
  bool _isLocked = false; bool _isSpeedActive = false; double _playbackSpeed = 1.0;
  List<SubtitleCue> _cues = []; String _activeSub = ''; Timer? _saveTimer;
  double _duration = 0.0; double _currentPosition = 0.0; bool _isDragging = false;
  bool _initError = false;

  @override
  void initState() {
    super.initState();
    SystemChrome.setPreferredOrientations([DeviceOrientation.landscapeRight, DeviceOrientation.landscapeLeft]);
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    _initPlayer();
  }

  // ✅ FIX: بناء URL صحيح للفيديو + معالجة أفضل للأخطاء
  String _resolveVideoUrl() {
    final candidates = [widget.videoUrl, widget.videoUrl1080, widget.videoUrl360];
    for (final url in candidates) {
      if (url.isNotEmpty) {
        if (url.startsWith('http')) return url;
        return 'https://movie.vodu.me/\$url';
      }
    }
    return '';
  }

  Future<void> _initPlayer() async {
    final url = _resolveVideoUrl();
    if (url.isEmpty) {
      if (mounted) setState(() => _initError = true);
      return;
    }
    try {
      // ✅ FIX: إضافة headers للـ VideoPlayer لتجاوز مشاكل الـ Android
      _controller = VideoPlayerController.networkUrl(
        Uri.parse(url),
        httpHeaders: {
          'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
          'Referer': 'https://movie.vodu.me/',
        },
      );
      await _controller!.initialize();
      _duration = _controller!.value.duration.inSeconds.toDouble();
      if (widget.startAt > 0) {
        await _controller!.seekTo(Duration(seconds: widget.startAt.toInt()));
      }
      _controller!.play();
      _isPlaying = true;
      if (mounted) setState(() {});
      _startAutoHide();
      _startSaveTimer();
      final subUrl = widget.subtitleVttUrl.isEmpty ? widget.subtitleUrl : widget.subtitleVttUrl;
      if (subUrl.isNotEmpty) {
        final cues = await SubtitleParser.parse(subUrl);
        if (mounted) setState(() => _cues = cues);
      }
      _controller!.addListener(_updatePosition);
    } catch (e) {
      if (mounted) setState(() => _initError = true);
    }
  }

  void _updatePosition() {
    if (_controller == null || !_controller!.value.isInitialized) return;
    if (!_isDragging && mounted) {
      setState(() => _currentPosition = _controller!.value.position.inSeconds.toDouble());
      final cue = _cues.firstWhere(
          (c) => _currentPosition >= c.startTime && _currentPosition <= c.endTime,
          orElse: () => SubtitleCue(startTime: 0, endTime: 0, text: ''));
      if (_activeSub != cue.text) setState(() => _activeSub = cue.text);
    }
  }

  void _startAutoHide() {
    _hideTimer?.cancel();
    _hideTimer = Timer(const Duration(seconds: 4), () {
      if (!_isLocked && mounted) setState(() => _showControls = false);
    });
  }

  void _startSaveTimer() {
    _saveTimer?.cancel();
    _saveTimer = Timer.periodic(const Duration(seconds: 5), (t) async {
      await WatchProgressStore().save(
        itemId: widget.itemId, title: widget.itemTitle, imageUrl: widget.itemImageUrl,
        episodeId: widget.episodeId, episodeTitle: widget.episodeTitle,
        progress: _currentPosition, duration: _duration,
        videoUrl: widget.videoUrl, videoUrl1080: widget.videoUrl1080,
        videoUrl360: widget.videoUrl360, subUrl: widget.subtitleUrl, subVttUrl: widget.subtitleVttUrl,
      );
    });
  }

  void _togglePlay() {
    if (_controller == null) return;
    setState(() {
      if (_isPlaying) _controller!.pause();
      else _controller!.play();
      _isPlaying = !_isPlaying;
    });
    _startAutoHide();
  }

  void _seek(double seconds) {
    _controller?.seekTo(Duration(seconds: seconds.toInt()));
    setState(() => _currentPosition = seconds);
    _startAutoHide();
  }

  void _seekDelta(double delta) {
    double newPos = _currentPosition + delta;
    if (newPos < 0) newPos = 0;
    if (newPos > _duration) newPos = _duration;
    _seek(newPos);
  }

  @override
  Widget build(BuildContext context) {
    if (_initError) {
      return Scaffold(
        backgroundColor: Colors.black,
        body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          const Icon(Icons.error_outline, color: Colors.red, size: 60),
          const SizedBox(height: 16),
          const Text('تعذّر تشغيل الفيديو', style: TextStyle(color: Colors.white, fontSize: 18)),
          const SizedBox(height: 16),
          CupertinoButton.filled(onPressed: () { setState(() { _initError = false; }); _initPlayer(); }, child: const Text('إعادة المحاولة')),
        ])),
      );
    }
    final settings = SettingsStore();
    return Scaffold(
      backgroundColor: Colors.black,
      body: GestureDetector(
        onTap: () {
          if (!_isLocked) {
            setState(() => _showControls = !_showControls);
            if (_showControls) _startAutoHide();
          }
        },
        onLongPressStart: (_) {
          if (!_isLocked) { setState(() => _isSpeedActive = true); _controller?.setPlaybackSpeed(2.0); }
        },
        onLongPressEnd: (_) {
          if (_isSpeedActive) { setState(() => _isSpeedActive = false); _controller?.setPlaybackSpeed(_playbackSpeed); }
        },
        child: Stack(
          children: [
            Center(
              child: (_controller != null && _controller!.value.isInitialized)
                  ? AspectRatio(aspectRatio: _controller!.value.aspectRatio, child: VideoPlayer(_controller!))
                  : const CircularProgressIndicator(color: Color(0xFFE50914)),
            ),
            if (_showControls || _isLocked) _buildControls(),
            if (settings.subtitlesEnabled && _activeSub.isNotEmpty)
              Positioned(
                bottom: settings.subtitleBottomPad, left: 16, right: 16,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: Colors.black.withOpacity(settings.subtitleBgOpacity),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(_activeSub,
                      style: TextStyle(
                        fontSize: settings.subtitleFontSize,
                        color: Color(int.parse(settings.subtitleColorHex.substring(1), radix: 16) + 0xFF000000),
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center),
                ),
              ),
            if (_isSpeedActive)
              const Positioned(
                top: 60, left: 0, right: 0,
                child: Center(child: Chip(
                  label: Text('2× سرعة', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  backgroundColor: Color(0xCCFF0000),
                )),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildControls() {
    return Container(
      color: Colors.black54,
      child: Column(
        children: [
          SafeArea(
            child: Row(
              children: [
                IconButton(icon: const Icon(Icons.arrow_back, color: Colors.white), onPressed: () => Navigator.pop(context)),
                const Spacer(),
                if (!_isLocked)
                  Text(
                    widget.episodeTitle.isEmpty ? widget.itemTitle : widget.episodeTitle,
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                  ),
                const Spacer(),
                IconButton(
                  icon: Icon(_isLocked ? Icons.lock : Icons.lock_open, color: Colors.white),
                  onPressed: () => setState(() => _isLocked = !_isLocked),
                ),
              ],
            ),
          ),
          const Spacer(),
          if (!_isLocked)
            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  Row(
                    children: [
                      Text(_formatTime(_currentPosition), style: const TextStyle(color: Colors.white)),
                      Expanded(
                        child: Slider(
                          value: _currentPosition.clamp(0.0, _duration > 0 ? _duration : 1.0),
                          min: 0, max: _duration > 0 ? _duration : 1.0,
                          onChanged: (v) => setState(() { _isDragging = true; _currentPosition = v; }),
                          onChangeEnd: (v) { _seek(v); _isDragging = false; },
                          activeColor: const Color(0xFFE50914),
                        ),
                      ),
                      Text(_formatTime(_duration), style: const TextStyle(color: Colors.white)),
                    ],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(icon: const Icon(Icons.replay_10, color: Colors.white, size: 30), onPressed: () => _seekDelta(-10)),
                      const SizedBox(width: 30),
                      IconButton(
                        icon: Icon(_isPlaying ? Icons.pause_circle_filled : Icons.play_circle_filled, color: Colors.white, size: 60),
                        onPressed: _togglePlay,
                      ),
                      const SizedBox(width: 30),
                      IconButton(icon: const Icon(Icons.forward_10, color: Colors.white, size: 30), onPressed: () => _seekDelta(10)),
                    ],
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }

  String _formatTime(double secs) {
    if (secs.isNaN || secs.isInfinite || secs < 0) return '00:00';
    final d = Duration(seconds: secs.toInt());
    return '\${d.inMinutes}:\${(d.inSeconds % 60).toString().padLeft(2, '0')}';
  }

  @override
  void dispose() {
    SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    _controller?.dispose();
    _hideTimer?.cancel();
    _saveTimer?.cancel();
    super.dispose();
  }
}
'''
with open(f"{BASE}/lib/screens/player_screen.dart", "w", encoding="utf-8") as f:
    f.write(player_screen)

print("✅ UTan v3.0.4 – تم إنشاء المشروع الكامل المُصحح في المجلد: " + BASE)
print()
print("🔧 ملخص الإصلاحات:")
print("   1. baseUrl بدون / في النهاية → منع double-slash في URLs")
print("   2. IOClient + HttpClient مُعدّل في كل الـ Services → تجاوز SSL موثوق على Android")
print("   3. إضافة Referer + Accept-Language + Connection headers")
print("   4. Retry تلقائي 3 مرات مع تأخير تدريجي عند الفشل")
print("   5. Timeout مُمدّد إلى 30 ثانية")
print("   6. VideoPlayerController مع httpHeaders صريحة")
print("   7. network_security_config محسّن مع trust-anchors")
print("   8. AndroidManifest مع صلاحيات Storage حسب API level")
print("   9. معالجة أفضل للأخطاء في PlayerScreen")
print("  10. pubspec محدّث: http: ^1.2.1 و google_fonts: ^6.1.0")
print()
print("🚀 للتشغيل:")
print("   cd " + BASE)
print("   flutter clean")
print("   flutter pub get")
print("   flutter run --release")