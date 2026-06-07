import os

# Create directory structure for Flutter project
BASE = "utan_flutter"
os.makedirs(f"{BASE}/lib/models", exist_ok=True)
os.makedirs(f"{BASE}/lib/services", exist_ok=True)
os.makedirs(f"{BASE}/lib/screens", exist_ok=True)
os.makedirs(f"{BASE}/lib/widgets", exist_ok=True)
os.makedirs(f"{BASE}/assets", exist_ok=True)
os.makedirs(f"{BASE}/.github/workflows", exist_ok=True)

# ============================================================
# 1. pubspec.yaml
# ============================================================
pubspec = """name: utan_flutter
description: UTan – Movie & TV streaming app (Flutter replica)
publish_to: 'none'
version: 3.0.0+3

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6
  http: ^1.1.0
  shared_preferences: ^2.2.2
  video_player: ^2.8.1
  path_provider: ^2.1.1
  dio: ^5.3.3
  permission_handler: ^11.0.1
  gallery_saver: ^2.3.2
  flutter_html: ^3.0.0-beta.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/
"""

with open(f"{BASE}/pubspec.yaml", "w", encoding="utf-8") as f:
    f.write(pubspec)

# ============================================================
# 2. lib/main.dart
# ============================================================
main_dart = """import 'package:flutter/material.dart';
import 'package:utan_flutter/screens/home_screen.dart';
import 'package:utan_flutter/screens/browse_screen.dart';
import 'package:utan_flutter/screens/search_screen.dart';
import 'package:utan_flutter/screens/downloads_screen.dart';
import 'package:utan_flutter/screens/settings_screen.dart';
import 'package:utan_flutter/services/settings_store.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SettingsStore.instance.init();
  runApp(const UTanApp());
}

class UTanApp extends StatelessWidget {
  const UTanApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'UTan',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0D0317),
        primaryColor: const Color(0xFFE30B1B),
        colorScheme: const ColorScheme.dark(primary: Color(0xFFE30B1B)),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0D0317),
          elevation: 0,
          centerTitle: true,
        ),
      ),
      home: const MainTabView(),
      debugShowCheckedModeBanner: false,
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
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _selectedIndex,
        onTap: (index) => setState(() => _selectedIndex = index),
        selectedItemColor: const Color(0xFFE30B1B),
        unselectedItemColor: Colors.grey,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'الرئيسية'),
          BottomNavigationBarItem(icon: Icon(Icons.grid_view), label: 'تصفح'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'بحث'),
          BottomNavigationBarItem(icon: Icon(Icons.download), label: 'التحميلات'),
          BottomNavigationBarItem(icon: Icon(Icons.more_horiz), label: 'المزيد'),
        ],
      ),
    );
  }
}
"""
with open(f"{BASE}/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(main_dart)

# ============================================================
# 3. Models
# ============================================================
# video_item.dart
video_item = """class VideoItem {
  final String id;
  final String title;
  final String imageUrl;
  final String type;

  VideoItem({required this.id, required this.title, required this.imageUrl, required this.type});

  Map<String, dynamic> toJson() => {'id': id, 'title': title, 'imageUrl': imageUrl, 'type': type};
  factory VideoItem.fromJson(Map<String, dynamic> json) => VideoItem(
        id: json['id'],
        title: json['title'],
        imageUrl: json['imageUrl'],
        type: json['type'],
      );
}
"""
with open(f"{BASE}/lib/models/video_item.dart", "w", encoding="utf-8") as f:
    f.write(video_item)

# episode.dart
episode = """class EpisodeItem {
  final String id;
  final String title;
  final String url;
  final String url1080;
  final String url360;
  final String subtitleUrl;
  final String subtitleVttUrl;

  EpisodeItem({
    required this.id,
    required this.title,
    required this.url,
    required this.url1080,
    required this.url360,
    required this.subtitleUrl,
    required this.subtitleVttUrl,
  });

  String get season {
    // Simplified season extraction (matches Swift logic)
    if (title.toLowerCase().contains('s')) {
      final match = RegExp(r'(S\\d+|موسم \\d+)', caseSensitive: false).firstMatch(title);
      if (match != null) return 'الموسم ' + match.group(0)!.replaceAll(RegExp(r'[^0-9]'), '');
    }
    return 'الموسم 1';
  }
}
"""
with open(f"{BASE}/lib/models/episode.dart", "w", encoding="utf-8") as f:
    f.write(episode)

# media_details.dart
media_details = """import 'package:utan_flutter/models/episode.dart';

class MediaDetails {
  String title;
  String imageUrl;
  String year;
  String genre;
  String rating;
  String runtime;
  String synopsis;
  bool isMovie;
  String movieUrl;
  String movieUrl1080;
  String movieUrl360;
  String movieSubtitleUrl;
  String movieSubtitleVttUrl;
  List<EpisodeItem> episodes;

  MediaDetails({
    this.title = '',
    this.imageUrl = '',
    this.year = '',
    this.genre = '',
    this.rating = '',
    this.runtime = '',
    this.synopsis = '',
    this.isMovie = true,
    this.movieUrl = '',
    this.movieUrl1080 = '',
    this.movieUrl360 = '',
    this.movieSubtitleUrl = '',
    this.movieSubtitleVttUrl = '',
    this.episodes = const [],
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
"""
with open(f"{BASE}/lib/models/media_details.dart", "w", encoding="utf-8") as f:
    f.write(media_details)

# watch_progress.dart
watch_progress = """import 'package:shared_preferences/shared_preferences.dart';

class WatchProgress {
  final String itemId;
  final String title;
  final String imageUrl;
  final String episodeId;
  final String episodeTitle;
  final double progressSeconds;
  final double durationSeconds;
  final DateTime updatedAt;
  final String videoUrl;
  final String videoUrl1080;
  final String videoUrl360;
  final String subtitleUrl;
  final String subtitleVttUrl;

  WatchProgress({
    required this.itemId,
    required this.title,
    required this.imageUrl,
    required this.episodeId,
    required this.episodeTitle,
    required this.progressSeconds,
    required this.durationSeconds,
    required this.updatedAt,
    required this.videoUrl,
    required this.videoUrl1080,
    required this.videoUrl360,
    required this.subtitleUrl,
    required this.subtitleVttUrl,
  });

  Map<String, dynamic> toJson() => {
        'itemId': itemId,
        'title': title,
        'imageUrl': imageUrl,
        'episodeId': episodeId,
        'episodeTitle': episodeTitle,
        'progressSeconds': progressSeconds,
        'durationSeconds': durationSeconds,
        'updatedAt': updatedAt.toIso8601String(),
        'videoUrl': videoUrl,
        'videoUrl1080': videoUrl1080,
        'videoUrl360': videoUrl360,
        'subtitleUrl': subtitleUrl,
        'subtitleVttUrl': subtitleVttUrl,
      };

  factory WatchProgress.fromJson(Map<String, dynamic> json) => WatchProgress(
        itemId: json['itemId'],
        title: json['title'],
        imageUrl: json['imageUrl'],
        episodeId: json['episodeId'],
        episodeTitle: json['episodeTitle'],
        progressSeconds: json['progressSeconds'],
        durationSeconds: json['durationSeconds'],
        updatedAt: DateTime.parse(json['updatedAt']),
        videoUrl: json['videoUrl'],
        videoUrl1080: json['videoUrl1080'],
        videoUrl360: json['videoUrl360'],
        subtitleUrl: json['subtitleUrl'],
        subtitleVttUrl: json['subtitleVttUrl'],
      );
}

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
    required String itemId,
    required String title,
    required String imageUrl,
    required String episodeId,
    required String episodeTitle,
    required double progress,
    required double duration,
    required String videoUrl,
    required String videoUrl1080,
    required String videoUrl360,
    required String subUrl,
    required String subVttUrl,
  }) async {
    _allProgress[itemId] = WatchProgress(
      itemId: itemId,
      title: title,
      imageUrl: imageUrl,
      episodeId: episodeId,
      episodeTitle: episodeTitle,
      progressSeconds: progress,
      durationSeconds: duration,
      updatedAt: DateTime.now(),
      videoUrl: videoUrl,
      videoUrl1080: videoUrl1080,
      videoUrl360: videoUrl360,
      subtitleUrl: subUrl,
      subtitleVttUrl: subVttUrl,
    );
    await _persist();
  }

  Future<void> remove(String itemId) async {
    _allProgress.remove(itemId);
    await _persist();
  }

  Future<void> clearAll() async {
    _allProgress.clear();
    await _persist();
  }

  WatchProgress? progress(String itemId) => _allProgress[itemId];

  List<WatchProgress> get recent => _allProgress.values.toList()
    ..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    final Map<String, dynamic> toSave = _allProgress.map((k, v) => MapEntry(k, v.toJson()));
    await prefs.setString(_key, jsonEncode(toSave));
  }
}

import 'dart:convert';
"""
with open(f"{BASE}/lib/models/watch_progress.dart", "w", encoding="utf-8") as f:
    f.write(watch_progress)

# download_task.dart
download_task = """class DownloadTaskItem {
  final String id;
  final String title;
  final String imageUrl;
  final bool isMovie;
  final String videoUrl;
  final String subtitleUrl;
  double progress;
  bool isCompleted;
  String? localVideoPath;

  DownloadTaskItem({
    required this.id,
    required this.title,
    required this.imageUrl,
    required this.isMovie,
    required this.videoUrl,
    required this.subtitleUrl,
    this.progress = 0.0,
    this.isCompleted = false,
    this.localVideoPath,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'imageUrl': imageUrl,
        'isMovie': isMovie,
        'videoUrl': videoUrl,
        'subtitleUrl': subtitleUrl,
        'progress': progress,
        'isCompleted': isCompleted,
        'localVideoPath': localVideoPath,
      };

  factory DownloadTaskItem.fromJson(Map<String, dynamic> json) => DownloadTaskItem(
        id: json['id'],
        title: json['title'],
        imageUrl: json['imageUrl'],
        isMovie: json['isMovie'],
        videoUrl: json['videoUrl'],
        subtitleUrl: json['subtitleUrl'],
        progress: json['progress'],
        isCompleted: json['isCompleted'],
        localVideoPath: json['localVideoPath'],
      );
}
"""
with open(f"{BASE}/lib/models/download_task.dart", "w", encoding="utf-8") as f:
    f.write(download_task)

# site_category.dart
site_category = """class SiteCategory {
  final int id;
  final String nameAr;
  final String nameEn;

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
"""
with open(f"{BASE}/lib/models/site_category.dart", "w", encoding="utf-8") as f:
    f.write(site_category)

# ============================================================
# 4. Services (simplified but complete)
# ============================================================
# scraper.dart
scraper_dart = """import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:utan_flutter/models/video_item.dart';
import 'package:utan_flutter/models/episode.dart';
import 'package:utan_flutter/models/media_details.dart';

class MovieScraper {
  static const String baseUrl = 'https://movie.vodu.me/';

  Future<({List<VideoItem> hero, List<Map<String, dynamic>> categories})> fetchHome() async {
    final response = await http.get(Uri.parse(baseUrl + 'index.php'));
    if (response.statusCode != 200) return (hero: [], categories: []);
    final html = response.body;
    // Simplified parsing – in real app use regex like Swift version
    // For brevity, we return mock data or minimal implementation.
    // Here we implement enough to make the app functional.
    List<VideoItem> hero = [];
    List<Map<String, dynamic>> categoryList = [];

    // Parse carousel images
    final carReg = RegExp(r'<a href="index\\.php\\?do=view&type=post&id=(\\d+)"><img src="([^"]+)"[^>]*alt="([^"]*)">');
    for (final match in carReg.allMatches(html)) {
      final id = match.group(1)!;
      var img = match.group(2)!;
      final title = match.group(3)!;
      if (!img.startsWith('http')) img = baseUrl + img;
      hero.add(VideoItem(id: id, title: title, imageUrl: img, type: 'post'));
    }

    // Parse category sections
    final sectionReg = RegExp(r'<h3[^>]*>\\s*([^<]+)\\s*</h3>.*?<div class="homeseries">(.*?)</div>\\s*</div>', dotAll: true);
    for (final match in sectionReg.allMatches(html)) {
      final secTitle = match.group(1)!.trim();
      final body = match.group(2)!;
      final items = _parseItemXBlock(body);
      if (items.isNotEmpty) {
        categoryList.add({'name': secTitle, 'items': items});
      }
    }
    return (hero: hero, categories: categoryList);
  }

  Future<List<VideoItem>> fetchCategory(int typeId, int page) async {
    final url = '$baseUrl/index.php?do=list&type=$typeId&page=$page';
    final response = await http.get(Uri.parse(url));
    if (response.statusCode != 200) return [];
    return _parseListPage(response.body);
  }

  Future<List<VideoItem>> search(String query) async {
    final encoded = Uri.encodeComponent(query);
    final url = '$baseUrl/index.php?do=list&title=$encoded';
    final response = await http.get(Uri.parse(url));
    if (response.statusCode != 200) return [];
    return _parseListPage(response.body);
  }

  Future<MediaDetails> fetchDetails(String id) async {
    final url = '$baseUrl/index.php?do=view&type=post&id=$id';
    final response = await http.get(Uri.parse(url));
    if (response.statusCode != 200) return MediaDetails();
    return _parseDetails(response.body);
  }

  List<VideoItem> _parseListPage(String html) {
    final List<VideoItem> items = [];
    final pattern = RegExp(r'href="index\\.php\\?do=view&type=post&id=(\\d+)"><img src="([^"]+)"[^>]*>\\s*</a>\\s*<div class="mytitle">\\s*<a[^>]*>([^<]+)</a>');
    for (final match in pattern.allMatches(html)) {
      final id = match.group(1)!;
      var img = match.group(2)!;
      final title = match.group(3)!.trim();
      if (!img.startsWith('http')) img = baseUrl + img;
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
      if (!img.startsWith('http')) img = baseUrl + img;
      items.add(VideoItem(id: 'home_${idx}_${title.substring(0, title.length > 10 ? 10 : title.length)}', title: title, imageUrl: img, type: 'post'));
      idx++;
    }
    return items;
  }

  MediaDetails _parseDetails(String html) {
    MediaDetails d = MediaDetails();
    // Title
    final titleMatch = RegExp(r'<h1>(.*?)</h1>').firstMatch(html);
    if (titleMatch != null) d.title = titleMatch.group(1)!;
    // Year
    final yearMatch = RegExp(r'<span>Year:\\s*</span>\\s*([^<]+)').firstMatch(html);
    if (yearMatch != null) d.year = yearMatch.group(1)!.trim();
    // Synopsis
    final synMatch = RegExp(r'<h3>Synopsis:</h3>.*?<h4>(.*?)</h4>', dotAll: true).firstMatch(html);
    if (synMatch != null) d.synopsis = synMatch.group(1)!.trim();
    // Image
    final imgMatch = RegExp(r'<img src="([^"]+)" class="img-responsive"').firstMatch(html);
    if (imgMatch != null) {
      var img = imgMatch.group(1)!;
      if (!img.startsWith('http')) img = baseUrl + img;
      d.imageUrl = img;
    }
    // Episodes
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
          id: id,
          title: title.isEmpty ? 'الحلقة ${episodes.length + 1}' : title,
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
      // Movie links
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
"""
with open(f"{BASE}/lib/services/scraper.dart", "w", encoding="utf-8") as f:
    f.write(scraper_dart)

# subtitle_parser.dart
subtitle_parser = """import 'package:http/http.dart' as http;

class SubtitleCue {
  final double startTime;
  final double endTime;
  final String text;

  SubtitleCue({required this.startTime, required this.endTime, required this.text});
}

class SubtitleParser {
  static Future<List<SubtitleCue>> parse(String url) async {
    if (url.isEmpty) return [];
    String clean = url;
    if (!clean.startsWith('http')) clean = 'https://movie.vodu.me/' + clean;
    final response = await http.get(Uri.parse(clean));
    if (response.statusCode != 200) return [];
    final String content = response.body;
    if (content.contains('WEBVTT')) return _parseWebVTT(content);
    return _parseSRT(content);
  }

  static List<SubtitleCue> _parseSRT(String content) {
    final List<SubtitleCue> cues = [];
    final blocks = content.split('\\n\\n');
    for (final block in blocks) {
      final lines = block.split('\\n').map((l) => l.trim()).where((l) => l.isNotEmpty).toList();
      if (lines.length < 3) continue;
      final timeLine = lines[1];
      final textLines = lines.sublist(2);
      final text = textLines.join('\\n').replaceAll(RegExp(r'<[^>]+>'), '').trim();
      if (text.isEmpty) continue;
      final times = timeLine.split(' --> ');
      if (times.length != 2) continue;
      final start = _parseSRTTime(times[0]);
      final end = _parseSRTTime(times[1]);
      if (start != null && end != null) {
        cues.add(SubtitleCue(startTime: start, endTime: end, text: text));
      }
    }
    return cues;
  }

  static double? _parseSRTTime(String timeStr) {
    final clean = timeStr.trim();
    final parts = clean.split(',');
    if (parts.length != 2) return null;
    final ms = double.tryParse(parts[1]);
    if (ms == null) return null;
    final timePart = parts[0];
    final comps = timePart.split(':');
    if (comps.length != 3) return null;
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
        if (times.length != 2) {
          i++;
          continue;
        }
        final start = _parseVTTTime(times[0]);
        final end = _parseVTTTime(times[1]);
        if (start != null && end != null) {
          final textLines = <String>[];
          i++;
          while (i < lines.length && lines[i].trim().isNotEmpty) {
            textLines.add(lines[i].trim());
            i++;
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
    final clean = timeStr.trim();
    final parts = clean.split(':');
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
"""
with open(f"{BASE}/lib/services/subtitle_parser.dart", "w", encoding="utf-8") as f:
    f.write(subtitle_parser)

# download_manager.dart (simplified using Dio)
download_manager = """import 'dart:io';
import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:gallery_saver/gallery_saver.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:utan_flutter/models/download_task.dart';

class DownloadManager {
  static final DownloadManager _instance = DownloadManager._internal();
  factory DownloadManager() => _instance;
  DownloadManager._internal();

  static const String _key = 'UTanDownloads_v1';
  List<DownloadTaskItem> _activeDownloads = [];
  final Dio _dio = Dio();

  List<DownloadTaskItem> get activeDownloads => List.unmodifiable(_activeDownloads);

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final String? data = prefs.getString(_key);
    if (data != null) {
      final List<dynamic> list = jsonDecode(data);
      _activeDownloads = list.map((e) => DownloadTaskItem.fromJson(e)).toList();
    }
  }

  Future<void> startDownload({
    required String id,
    required String title,
    required String imageUrl,
    required bool isMovie,
    required String videoUrl,
    required String subtitleUrl,
  }) async {
    if (_activeDownloads.any((d) => d.id == id)) return;
    final task = DownloadTaskItem(
      id: id,
      title: title,
      imageUrl: imageUrl,
      isMovie: isMovie,
      videoUrl: videoUrl,
      subtitleUrl: subtitleUrl,
    );
    _activeDownloads.add(task);
    await _persist();

    // Request storage permission
    await Permission.storage.request();

    final dir = await getTemporaryDirectory();
    final savePath = '${dir.path}/$id.mp4';
    await _dio.download(videoUrl, savePath, onReceiveProgress: (received, total) {
      final index = _activeDownloads.indexWhere((d) => d.id == id);
      if (index != -1) {
        _activeDownloads[index].progress = received / total;
        _persist();
      }
    });
    // Mark completed
    final idx = _activeDownloads.indexWhere((d) => d.id == id);
    if (idx != -1) {
      _activeDownloads[idx].isCompleted = true;
      _activeDownloads[idx].localVideoPath = savePath;
      await _persist();
      // Save to gallery
      await GallerySaver.saveVideo(savePath, toDcim: true);
    }
  }

  Future<void> cancel(String id) async {
    _activeDownloads.removeWhere((d) => d.id == id);
    await _persist();
  }

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    final List<Map<String, dynamic>> list = _activeDownloads.map((e) => e.toJson()).toList();
    await prefs.setString(_key, jsonEncode(list));
  }
}

import 'dart:convert';
"""
with open(f"{BASE}/lib/services/download_manager.dart", "w", encoding="utf-8") as f:
    f.write(download_manager)

# progress_store.dart (re-export watch_progress)
progress_store_dart = """export '../models/watch_progress.dart';
"""
with open(f"{BASE}/lib/services/progress_store.dart", "w", encoding="utf-8") as f:
    f.write(progress_store_dart)

# favorites_store.dart
favorites_store = """import 'package:shared_preferences/shared_preferences.dart';
import 'package:utan_flutter/models/video_item.dart';

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
    if (index != -1) {
      _items.removeAt(index);
    } else {
      _items.insert(0, item);
    }
    await _persist();
  }

  bool isFavorite(String id) => _items.any((i) => i.id == id);

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    final List<Map<String, dynamic>> list = _items.map((e) => e.toJson()).toList();
    await prefs.setString(_key, jsonEncode(list));
  }
}

import 'dart:convert';
"""
with open(f"{BASE}/lib/services/favorites_store.dart", "w", encoding="utf-8") as f:
    f.write(favorites_store)

# settings_store.dart
settings_store = """import 'package:shared_preferences/shared_preferences.dart';

class SettingsStore {
  static final SettingsStore _instance = SettingsStore._internal();
  factory SettingsStore() => _instance;
  SettingsStore._internal();

  static const String keyFontSize = 'sub_fontSize';
  static const String keyColorHex = 'sub_colorHex';
  static const String keyBgOpacity = 'sub_bgOpacity';
  static const String keyBottomPad = 'sub_bottomPad';
  static const String keyEnabled = 'sub_enabled';

  double subtitleFontSize = 22.0;
  String subtitleColorHex = '#FFFFFF';
  double subtitleBgOpacity = 0.6;
  double subtitleBottomPad = 60.0;
  bool subtitlesEnabled = true;

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    subtitleFontSize = prefs.getDouble(keyFontSize) ?? 22.0;
    subtitleColorHex = prefs.getString(keyColorHex) ?? '#FFFFFF';
    subtitleBgOpacity = prefs.getDouble(keyBgOpacity) ?? 0.6;
    subtitleBottomPad = prefs.getDouble(keyBottomPad) ?? 60.0;
    subtitlesEnabled = prefs.getBool(keyEnabled) ?? true;
  }

  Future<void> save() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble(keyFontSize, subtitleFontSize);
    await prefs.setString(keyColorHex, subtitleColorHex);
    await prefs.setDouble(keyBgOpacity, subtitleBgOpacity);
    await prefs.setDouble(keyBottomPad, subtitleBottomPad);
    await prefs.setBool(keyEnabled, subtitlesEnabled);
  }
}
"""
with open(f"{BASE}/lib/services/settings_store.dart", "w", encoding="utf-8") as f:
    f.write(settings_store)

# ============================================================
# 5. Screens (minimal implementations – can be extended)
# ============================================================
# home_screen.dart
home_screen = """import 'package:flutter/material.dart';
import 'package:utan_flutter/services/scraper.dart';
import 'package:utan_flutter/services/progress_store.dart';
import 'package:utan_flutter/widgets/hero_banner.dart';
import 'package:utan_flutter/widgets/continue_row.dart';
import 'package:utan_flutter/widgets/category_row.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final MovieScraper _scraper = MovieScraper();
  bool _loading = true;
  List<dynamic> _heroItems = [];
  List<Map<String, dynamic>> _categories = [];

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    final data = await _scraper.fetchHome();
    setState(() {
      _heroItems = data.hero;
      _categories = data.categories;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }
    return Scaffold(
      backgroundColor: const Color(0xFF0D0317),
      body: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: HeroBanner(items: _heroItems),
          ),
          SliverToBoxAdapter(
            child: ContinueWatchingRow(),
          ),
          SliverList(
            delegate: SliverChildBuilderDelegate(
              (context, index) {
                final cat = _categories[index];
                return CategoryRow(
                  title: cat['name'],
                  items: cat['items'],
                );
              },
              childCount: _categories.length,
            ),
          ),
        ],
      ),
    );
  }
}
"""
with open(f"{BASE}/lib/screens/home_screen.dart", "w", encoding="utf-8") as f:
    f.write(home_screen)

# browse_screen.dart
browse_screen = """import 'package:flutter/material.dart';
import 'package:utan_flutter/models/site_category.dart';
import 'package:utan_flutter/screens/details_screen.dart';

class BrowseScreen extends StatelessWidget {
  const BrowseScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0317),
      appBar: AppBar(title: const Text('تصفح')),
      body: GridView.builder(
        padding: const EdgeInsets.all(12),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
          childAspectRatio: 1.5
