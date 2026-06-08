import os

BASE = "utan_flutter"

# إنشاء المجلدات الأساسية
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

# ==================== 1. pubspec.yaml ====================
# تم إضافة حزم cronet_http و cupertino_http للاتصال الأصلي
pubspec = '''name: utan_flutter
description: UTan – Full Android replica of iOS version
publish_to: 'none'
version: 3.0.3+8

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6
  http: ^1.2.0
  cronet_http: ^1.0.0
  cupertino_http: ^1.3.0
  shared_preferences: ^2.2.2
  video_player: ^2.8.1
  path_provider: ^2.1.1
  dio: ^5.3.3
  permission_handler: ^11.0.1
  gallery_saver: ^2.3.2
  google_fonts: ^4.0.4
  cached_network_image: ^3.3.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
'''
with open(f"{BASE}/pubspec.yaml", "w", encoding="utf-8") as f:
    f.write(pubspec)

# ==================== 2. network_security_config.xml ====================
# تم إضافة <certificates src="raw" /> لكي يقبل مشغل الفيديو (ExoPlayer) السيرفرات المحلية
network_security = '''<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">movie.vodu.me</domain>
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
            <certificates src="raw" />
        </trust-anchors>
    </domain-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
            <certificates src="raw" />
        </trust-anchors>
    </base-config>
</network-security-config>
'''
with open(f"{BASE}/android/app/src/main/res/xml/network_security_config.xml", "w", encoding="utf-8") as f:
    f.write(network_security)

# ==================== 3. AndroidManifest.xml ====================
android_manifest = '''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    <application
        android:label="UTan"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher"
        android:usesCleartextTraffic="true"
        android:networkSecurityConfig="@xml/network_security_config">
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

# ==================== 4. main.dart ====================
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

class InsecureHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback = (X509Certificate cert, String host, int port) => true;
  }
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
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

# ==================== 5. Models ====================
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
        progressSeconds: json['progressSeconds'], durationSeconds: json['durationSeconds'],
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
        progress: json['progress'], isCompleted: json['isCompleted'], localVideoPath: json['localVideoPath'],
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

# ==================== 6. Services ====================

# 6.1 scraper.dart (معدل لتخطي JA3 باستخدام Native Clients)
scraper_dart = '''import 'dart:async';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http/io_client.dart';
import 'package:cronet_http/cronet_http.dart';
import 'package:cupertino_http/cupertino_http.dart';
import '../models/video_item.dart';
import '../models/episode.dart';
import '../models/media_details.dart';

class MovieScraper {
  static const String baseUrl = 'https://movie.vodu.me';
  static const String userAgent = 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36';

  // 🔥 هنا السر: استخدام محرك النظام الأصلي لتجاوز حظر البصمة (JA3 Bypass)
  static http.Client _createClient() {
    if (Platform.isAndroid) {
      try {
        final engine = CronetEngine.build(cacheMode: CacheMode.memory, cacheMaxSize: 1048576);
        return CronetClient.fromCronetEngine(engine);
      } catch (e) {
        return _fallbackClient();
      }
    } else if (Platform.isIOS) {
      try {
        final config = URLSessionConfiguration.ephemeralSessionConfiguration()..allowsCellularAccess = true;
        return CupertinoClient.fromSessionConfiguration(config);
      } catch (e) {
        return _fallbackClient();
      }
    }
    return _fallbackClient();
  }

  static http.Client _fallbackClient() {
    final client = HttpClient()
      ..badCertificateCallback = (cert, host, port) => true
      ..connectionTimeout = const Duration(seconds: 30);
    return IOClient(client);
  }

  static Future<http.Response> _getWithRetry(String url, {int retries = 3}) async {
    for (int attempt = 1; attempt <= retries; attempt++) {
      final client = _createClient();
      try {
        final response = await client.get(
          Uri.parse(url),
          headers: {
            'User-Agent': userAgent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
            'Referer': '$baseUrl/',
            'Connection': 'keep-alive',
          },
        ).timeout(const Duration(seconds: 30));
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

  Future<({List<VideoItem> hero, List<Map<String, dynamic>> categories})> fetchHome() async {
    try {
      final response = await _getWithRetry('$baseUrl/index.php');
      if (response.statusCode != 200) throw Exception('HTTP ${response.statusCode}');
      final html = response.body;
      List<VideoItem> hero = [];
      List<Map<String, dynamic>> categoryList = [];

      final carReg = RegExp(r'<a href="index\\.php\\?do=view&type=post&id=(\\d+)"><img src="([^"]+)"[^>]*alt="([^"]*)"');
      for (final match in carReg.allMatches(html)) {
        final id = match.group(1)!;
        var img = match.group(2)!;
        final title = match.group(3)!;
        if (!img.startsWith('http')) img = '$baseUrl/$img';
        hero.add(VideoItem(id: id, title: title, imageUrl: img, type: 'post'));
      }

      final sectionReg = RegExp(r'<h3[^>]*>\\s*([^<]+)\\s*</h3>.*?<div class="homeseries">(.*?)</div>\\s*</div>', dotAll: true);
      for (final match in sectionReg.allMatches(html)) {
        final secTitle = match.group(1)!.trim();
        final body = match.group(2)!;
        final items = _parseItemXBlock(body);
        if (items.isNotEmpty) categoryList.add({'name': secTitle, 'items': items});
      }

      if (categoryList.isEmpty && hero.isNotEmpty) {
        categoryList.add({'name': 'الرائج الآن', 'items': hero.take(10).toList()});
      }
      return (hero: hero, categories: categoryList);
    } catch (e) {
      print('Scraper Error Home: $e');
      return (hero: <VideoItem>[], categories: <Map<String, dynamic>>[]);
    }
  }

  Future<List<VideoItem>> fetchCategory(int typeId, int page) async {
    try {
      final url = '$baseUrl/index.php?do=list&type=$typeId&page=$page';
      final response = await _getWithRetry(url);
      if (response.statusCode != 200) return [];
      return _parseListPage(response.body);
    } catch (e) { return []; }
  }

  Future<List<VideoItem>> search(String query) async {
    try {
      final encoded = Uri.encodeComponent(query);
      final url = '$baseUrl/index.php?do=list&title=$encoded';
      final response = await _getWithRetry(url);
      if (response.statusCode != 200) return [];
      return _parseListPage(response.body);
    } catch (e) { return []; }
  }

  Future<MediaDetails> fetchDetails(String id) async {
    try {
      final url = '$baseUrl/index.php?do=view&type=post&id=$id';
      final response = await _getWithRetry(url);
      if (response.statusCode != 200) return MediaDetails();
      return _parseDetails(response.body);
    } catch (e) {
      return MediaDetails(title: 'حدث خطأ في جلب البيانات');
    }
  }

  List<VideoItem> _parseListPage(String html) {
    final List<VideoItem> items = [];
    final pattern = RegExp(r'href="index\\.php\\?do=view&type=post&id=(\\d+)"><img src="([^"]+)"[^>]*>\\s*</a>\\s*<div class="mytitle">\\s*<a[^>]*>([^<]+)</a>');
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
    final pattern = RegExp(r'<div class="itemx"[^>]*>.*?<img src="([^"]+)".*?<div class="mytitle">([^<]+)</div>', dotAll: true);
    int idx = 1;
    for (final match in pattern.allMatches(html)) {
      var img = match.group(1)!;
      final title = match.group(2)!.trim();
      if (!img.startsWith('http')) img = '$baseUrl/$img';
      items.add(VideoItem(id: 'home_${idx}_${title.substring(0, title.length > 10 ? 10 : title.length)}', title: title, imageUrl: img, type: 'post'));
      idx++;
    }
    return items;
  }

  MediaDetails _parseDetails(String html) {
    MediaDetails d = MediaDetails();
    final titleMatch = RegExp(r'<h1>(.*?)</h1>').firstMatch(html);
    if (titleMatch != null) d.title = titleMatch.group(1)!;
    final yearMatch = RegExp(r'<span>Year:\\s*</span>\\s*([^<]+)').firstMatch(html);
    if (yearMatch != null) d.year = yearMatch.group(1)!.trim();
    final genreMatch = RegExp(r'<span>Genre:\\s*</span>\\s*([^<]+)').firstMatch(html);
    if (genreMatch != null) d.genre = genreMatch.group(1)!.trim();
    final ratingMatch = RegExp(r'<span>IMdB Rating:\\s*</span>\\s*([^<]+)').firstMatch(html);
    if (ratingMatch != null) d.rating = ratingMatch.group(1)!.trim();
    final runtimeMatch = RegExp(r'<span>Runtime:\\s*</span>\\s*([^<]+)').firstMatch(html);
    if (runtimeMatch != null) d.runtime = runtimeMatch.group(1)!.trim();
    final synopsisMatch = RegExp(r'<h3>Synopsis:</h3>.*?<h4>(.*?)</h4>', dotAll: true).firstMatch(html);
    if (synopsisMatch != null) d.synopsis = synopsisMatch.group(1)!.trim();
    final imgMatch = RegExp(r'<img src="([^"]+)" class="img-responsive"').firstMatch(html);
    if (imgMatch != null) {
      var img = imgMatch.group(1)!;
      if (!img.startsWith('http')) img = '$baseUrl/$img';
      d.imageUrl = img;
    }
    final epBlock = RegExp(r'<li class="episodeitem">(.*?)</li>', dotAll: true);
    final episodes = <EpisodeItem>[];
    for (final match in epBlock.allMatches(html)) {
      final block = match.group(1)!;
      final id = RegExp(r'data-id="(\\d+)"').firstMatch(block)?.group(1) ?? '';
      if (id.isEmpty) continue;
      final title = RegExp(r'data-title="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final url = RegExp(r'data-url="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final url360 = RegExp(r'data-url360="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final url1080 = RegExp(r'data-url1080="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final srt = RegExp(r'data-srt="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      final vtt = RegExp(r'data-webvtt="([^"]*)"').firstMatch(block)?.group(1) ?? '';
      if (url.isNotEmpty) {
        episodes.add(EpisodeItem(
          id: id, title: title.isEmpty ? 'الحلقة ${episodes.length + 1}' : title,
          url: url, url1080: url1080, url360: url360, subtitleUrl: srt, subtitleVttUrl: vtt,
        ));
      }
    }
    if (episodes.isNotEmpty) {
      d.isMovie = false;
      d.episodes = episodes;
    } else {
      final movieMatch = RegExp(r'data-url="([^"]+)"[^>]*data-url360="([^"]*)"[^>]*data-url1080="([^"]*)"[^>]*data-srt="([^"]*)"[^>]*data-webvtt="([^"]*)"').firstMatch(html);
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

# 6.2 subtitle_parser.dart (معدل لتخطي JA3)
subtitle_parser = '''import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http/io_client.dart';
import 'package:cronet_http/cronet_http.dart';
import 'package:cupertino_http/cupertino_http.dart';

class SubtitleCue {
  final double startTime; final double endTime; final String text;
  SubtitleCue({required this.startTime, required this.endTime, required this.text});
}

class SubtitleParser {
  static http.Client _buildClient() {
    if (Platform.isAndroid) {
      try {
        final engine = CronetEngine.build(cacheMode: CacheMode.memory, cacheMaxSize: 1048576);
        return CronetClient.fromCronetEngine(engine);
      } catch (e) {
        return _fallbackClient();
      }
    } else if (Platform.isIOS) {
      try {
        final config = URLSessionConfiguration.ephemeralSessionConfiguration()..allowsCellularAccess = true;
        return CupertinoClient.fromSessionConfiguration(config);
      } catch (e) {
        return _fallbackClient();
      }
    }
    return _fallbackClient();
  }

  static http.Client _fallbackClient() {
    final client = HttpClient()
      ..badCertificateCallback = (cert, host, port) => true
      ..connectionTimeout = const Duration(seconds: 20);
    return IOClient(client);
  }

  static Future<List<SubtitleCue>> parse(String url) async {
    if (url.isEmpty) return [];
    String clean = url;
    if (!clean.startsWith('http')) clean = 'https://movie.vodu.me/$clean';
    final client = _buildClient();
    try {
      final response = await client.get(
        Uri.parse(clean),
        headers: {
          'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
          'Referer': 'https://movie.vodu.me/',
        },
      ).timeout(const Duration(seconds: 20));
      client.close();
      if (response.statusCode != 200) return [];
      final content = response.body;
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
    final h = double.tryParse(comps[0]) ?? 0; final m = double.tryParse(comps[1]) ?? 0; final s = double.tryParse(comps[2]) ?? 0;
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
          while (i < lines.length && lines[i].trim().isNotEmpty) { textLines.add(lines[i].trim()); i++; }
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
      h = double.tryParse(parts[0]) ?? 0; m = double.tryParse(parts[1]) ?? 0;
      final secParts = parts[2].split('.');
      s = double.tryParse(secParts[0]) ?? 0;
      if (secParts.length == 2) s += (double.tryParse(secParts[1]) ?? 0) / 1000;
    } else if (parts.length == 2) {
      m = double.tryParse(parts[0]) ?? 0; final secParts = parts[1].split('.');
      s = double.tryParse(secParts[0]) ?? 0;
      if (secParts.length == 2) s += (double.tryParse(secParts[1]) ?? 0) / 1000;
    } else return null;
    return h * 3600 + m * 60 + s;
  }
}
'''
with open(f"{BASE}/lib/services/subtitle_parser.dart", "w", encoding="utf-8") as f:
    f.write(subtitle_parser)

# 6.3 progress_store.dart
progress_store = '''import 'dart:convert';
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
'''
with open(f"{BASE}/lib/services/progress_store.dart", "w", encoding="utf-8") as f:
    f.write(progress_store)

# 6.4 download_manager.dart (مكتمل ومحدث لـ Dio v5+)
download_manager = '''import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:dio/io.dart';
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
  late Dio _dio;
  List<DownloadTaskItem> get activeDownloads => List.unmodifiable(_activeDownloads);

  Future<void> init() async {
    _dio = Dio(BaseOptions(
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 0),
      headers: {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
        'Referer': 'https://movie.vodu.me/',
      },
    ));
    
    // 🔥 تحديث متوافق مع Dio الإصدار الخامس فما فوق لتخطي حماية SSL أثناء التحميل
    _dio.httpClientAdapter = IOHttpClientAdapter(
      createHttpClient: () {
        final client = HttpClient();
        client.badCertificateCallback = (X509Certificate cert, String host, int port) => true;
        return client;
      },
    );

    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(_key);
    if (data != null) {
      final List decoded = jsonDecode(data);
      _activeDownloads = decoded.map((v) => DownloadTaskItem.fromJson(v)).toList();
    }
  }

  Future<void> startDownload(DownloadTaskItem item) async {
    if (_activeDownloads.any((element) => element.id == item.id)) return;
    _activeDownloads.add(item);
    await _persist();
    
    try {
      if (await Permission.storage.request().isGranted || await Permission.photos.request().isGranted) {
        final dir = await getApplicationDocumentsDirectory();
        final savePath = '${dir.path}/${item.title.replaceAll(' ', '_')}.mp4';
        
        await _dio.download(
          item.videoUrl,
          savePath,
          onReceiveProgress: (received, total) {
            if (total != -1) {
              item.progress = received / total;
              _persist(); // يمكن تفعيله ولكن قد يسبب ضغط على المعالج، يفضل تحديث الواجهة فقط
            }
          },
        );
        
        item.isCompleted = true;
        item.localVideoPath = savePath;
        await GallerySaver.saveVideo(savePath); // حفظ بالمعرض لتطابق نسخة iOS
        await _persist();
      }
    } catch (e) {
      _activeDownloads.removeWhere((element) => element.id == item.id);
      await _persist();
    }
  }

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, jsonEncode(_activeDownloads.map((e) => e.toJson()).toList()));
  }
}
'''
with open(f"{BASE}/lib/services/download_manager.dart", "w", encoding="utf-8") as f:
    f.write(download_manager)

# ==================== 7. Missing UI & Stores (Essential for Compile) ====================
# توفير الـ Stubs للواجهات حتى يعمل الكود بدون أي File Not Found Errors

# 7.1 settings_store.dart
settings_store = '''import 'package:shared_preferences/shared_preferences.dart';
class SettingsStore {
  static final SettingsStore _instance = SettingsStore._internal();
  factory SettingsStore() => _instance;
  SettingsStore._internal();
  Future<void> init() async {}
}
'''
with open(f"{BASE}/lib/services/settings_store.dart", "w", encoding="utf-8") as f:
    f.write(settings_store)

# 7.2 favorites_store.dart
favorites_store = '''import 'package:shared_preferences/shared_preferences.dart';
class FavoritesStore {
  static final FavoritesStore _instance = FavoritesStore._internal();
  factory FavoritesStore() => _instance;
  FavoritesStore._internal();
  Future<void> init() async {}
}
'''
with open(f"{BASE}/lib/services/favorites_store.dart", "w", encoding="utf-8") as f:
    f.write(favorites_store)

# 7.3 Basic Screens
basic_screen = '''import 'package:flutter/material.dart';
class {className} extends StatelessWidget {{
  const {className}({{super.key}});
  @override
  Widget build(BuildContext context) {{
    return const Center(child: Text('{title}', style: TextStyle(color: Colors.white, fontSize: 24)));
  }}
}}
'''

screens = {
    "home_screen.dart": ("HomeScreen", "الرئيسية"),
    "browse_screen.dart": ("BrowseScreen", "التصفح"),
    "search_screen.dart": ("SearchScreen", "البحث"),
    "downloads_screen.dart": ("DownloadsScreen", "التحميلات"),
    "settings_screen.dart": ("SettingsScreen", "الإعدادات"),
}

for fname, (cls_name, title) in screens.items():
    with open(f"{BASE}/lib/screens/{fname}", "w", encoding="utf-8") as f:
        f.write(basic_screen.format(className=cls_name, title=title))

print("✅ تمت كتابة الملفات بنجاح. الكود جاهز للتشغيل على Android و iOS.")