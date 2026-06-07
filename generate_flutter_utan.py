import os

BASE = "utan_flutter"

# Create directory structure
dirs = [
    f"{BASE}/lib/models",
    f"{BASE}/lib/services",
    f"{BASE}/lib/screens",
    f"{BASE}/lib/widgets",
    f"{BASE}/assets",
    f"{BASE}/.github/workflows",
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# =============================================================================
# pubspec.yaml (corrected http version)
# =============================================================================
pubspec = '''name: utan_flutter
description: UTan – Movie & TV streaming app (Flutter replica)
publish_to: 'none'
version: 3.0.0+3

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6
  http: ^0.13.6
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
'''
with open(f"{BASE}/pubspec.yaml", "w") as f:
    f.write(pubspec)

# =============================================================================
# lib/main.dart
# =============================================================================
main_dart = '''import 'package:flutter/material.dart';
import 'package:utan_flutter/screens/home_screen.dart';
import 'package:utan_flutter/screens/browse_screen.dart';
import 'package:utan_flutter/screens/search_screen.dart';
import 'package:utan_flutter/screens/downloads_screen.dart';
import 'package:utan_flutter/screens/settings_screen.dart';
import 'package:utan_flutter/services/settings_store.dart';
import 'package:utan_flutter/services/progress_store.dart';
import 'package:utan_flutter/services/favorites_store.dart';
import 'package:utan_flutter/services/download_manager.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
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
'''
with open(f"{BASE}/lib/main.dart", "w") as f:
    f.write(main_dart)

# =============================================================================
# MODELS (all corrected)
# =============================================================================
# video_item.dart
with open(f"{BASE}/lib/models/video_item.dart", "w") as f:
    f.write('''class VideoItem {
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
''')

# episode.dart
with open(f"{BASE}/lib/models/episode.dart", "w") as f:
    f.write('''class EpisodeItem {
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
''')

# media_details.dart
with open(f"{BASE}/lib/models/media_details.dart", "w") as f:
    f.write('''import 'package:utan_flutter/models/episode.dart';

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
''')

# watch_progress.dart
with open(f"{BASE}/lib/models/watch_progress.dart", "w") as f:
    f.write('''import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

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
''')

# download_task.dart
with open(f"{BASE}/lib/models/download_task.dart", "w") as f:
    f.write('''class DownloadTaskItem {
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
''')

# site_category.dart
with open(f"{BASE}/lib/models/site_category.dart", "w") as f:
    f.write('''class SiteCategory {
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
''')

# =============================================================================
# SERVICES (corrected)
# =============================================================================
# scraper.dart – fixed return types
scraper_dart = '''import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:utan_flutter/models/video_item.dart';
import 'package:utan_flutter/models/episode.dart';
import 'package:utan_flutter/models/media_details.dart';

class MovieScraper {
  static const String baseUrl = 'https://movie.vodu.me/';

  Future<({List<VideoItem> hero, List<Map<String, dynamic>> categories})> fetchHome() async {
    final response = await http.get(Uri.parse(baseUrl + 'index.php'));
    if (response.statusCode != 200) {
      return (hero: <VideoItem>[], categories: <Map<String, dynamic>>[]);
    }
    final html = response.body;
    List<VideoItem> hero = <VideoItem>[];
    List<Map<String, dynamic>> categoryList = <Map<String, dynamic>>[];

    final carReg = RegExp(r'<a href="index\\.php\\?do=view&type=post&id=(\\d+)"><img src="([^"]+)"[^>]*alt="([^"]*)">');
    for (final match in carReg.allMatches(html)) {
      final id = match.group(1)!;
      var img = match.group(2)!;
      final title = match.group(3)!;
      if (!img.startsWith('http')) img = baseUrl + img;
      hero.add(VideoItem(id: id, title: title, imageUrl: img, type: 'post'));
    }

    final sectionReg = RegExp(r'<h3[^>]*>\\s*([^<]+)\\s*</h3>.*?<div class="homeseries">(.*?)</div>\\s*</div>', dotAll: true);
    for (final match in sectionReg.allMatches(html)) {
      final secTitle = match.group(1)!.trim();
      final body = match.group(2)!;
      final items = _parseItemXBlock(body);
      if (items.isNotEmpty) {
        categoryList.add({'name': secTitle, 'items': items});
      }
    }

    if (categoryList.isEmpty && hero.isNotEmpty) {
      categoryList.add({'name': 'الرائج الآن', 'items': hero.take(10).toList()});
    }

    return (hero: hero, categories: categoryList);
  }

  Future<List<VideoItem>> fetchCategory(int typeId, int page) async {
    final url = '$baseUrl/index.php?do=list&type=$typeId&page=$page';
    final response = await http.get(Uri.parse(url));
    if (response.statusCode != 200) return <VideoItem>[];
    return _parseListPage(response.body);
  }

  Future<List<VideoItem>> search(String query) async {
    final encoded = Uri.encodeComponent(query);
    final url = '$baseUrl/index.php?do=list&title=$encoded';
    final response = await http.get(Uri.parse(url));
    if (response.statusCode != 200) return <VideoItem>[];
    return _parseListPage(response.body);
  }

  Future<MediaDetails> fetchDetails(String id) async {
    final url = '$baseUrl/index.php?do=view&type=post&id=$id';
    final response = await http.get(Uri.parse(url));
    if (response.statusCode != 200) return MediaDetails();
    return _parseDetails(response.body);
  }

  List<VideoItem> _parseListPage(String html) {
    final List<VideoItem> items = <VideoItem>[];
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
    final List<VideoItem> items = <VideoItem>[];
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
    final synMatch = RegExp(r'<h3>Synopsis:</h3>.*?<h4>(.*?)</h4>', dotAll: true).firstMatch(html);
    if (synMatch != null) d.synopsis = synMatch.group(1)!.trim();
    final imgMatch = RegExp(r'<img src="([^"]+)" class="img-responsive"').firstMatch(html);
    if (imgMatch != null) {
      var img = imgMatch.group(1)!;
      if (!img.startsWith('http')) img = baseUrl + img;
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
with open(f"{BASE}/lib/services/scraper.dart", "w") as f:
    f.write(scraper_dart)

# subtitle_parser.dart (no changes, already correct)
subtitle_parser = '''import 'package:http/http.dart' as http;

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
'''
with open(f"{BASE}/lib/services/subtitle_parser.dart", "w") as f:
    f.write(subtitle_parser)

# download_manager.dart (no changes)
download_manager = '''import 'dart:convert';
import 'dart:io';
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
    final idx = _activeDownloads.indexWhere((d) => d.id == id);
    if (idx != -1) {
      _activeDownloads[idx].isCompleted = true;
      _activeDownloads[idx].localVideoPath = savePath;
      await _persist();
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
'''
with open(f"{BASE}/lib/services/download_manager.dart", "w") as f:
    f.write(download_manager)

# progress_store.dart (re-export)
with open(f"{BASE}/lib/services/progress_store.dart", "w") as f:
    f.write("export '../models/watch_progress.dart';")

# favorites_store.dart (fixed: use factory constructor)
favorites_store = '''import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
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
'''
with open(f"{BASE}/lib/services/favorites_store.dart", "w") as f:
    f.write(favorites_store)

# settings_store.dart (fixed: use factory constructor)
settings_store = '''import 'package:shared_preferences/shared_preferences.dart';

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
'''
with open(f"{BASE}/lib/services/settings_store.dart", "w") as f:
    f.write(settings_store)

# =============================================================================
# WIDGETS (corrected type annotations)
# =============================================================================
# poster_card.dart (no changes, already correct)
with open(f"{BASE}/lib/widgets/poster_card.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/models/watch_progress.dart';
import 'package:utan_flutter/models/video_item.dart';

class PosterCard extends StatelessWidget {
  final VideoItem item;
  final WatchProgress? progress;

  const PosterCard({super.key, required this.item, this.progress});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 120,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Stack(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Image.network(
                  item.imageUrl,
                  width: 120,
                  height: 180,
                  fit: BoxFit.cover,
                  errorBuilder: (_, __, ___) => Container(color: Colors.grey[800]),
                ),
              ),
              Positioned.fill(
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    gradient: const LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [Colors.transparent, Colors.black54],
                    ),
                  ),
                ),
              ),
              if (progress != null && progress!.durationSeconds > 0)
                Positioned(
                  bottom: 0,
                  left: 0,
                  right: 0,
                  child: LinearProgressIndicator(
                    value: progress!.progressSeconds / progress!.durationSeconds,
                    backgroundColor: Colors.white30,
                    valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFFE30B1B)),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 6),
          Text(
            item.title,
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.white),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}
''')

# hero_banner.dart (fix List<VideoItem> type)
with open(f"{BASE}/lib/widgets/hero_banner.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/models/video_item.dart';
import 'package:utan_flutter/screens/details_screen.dart';
import 'package:utan_flutter/services/favorites_store.dart';

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
    if (_controller.hasClients && widget.items.length > 1) {
      _controller.nextPage(duration: const Duration(milliseconds: 800), curve: Curves.easeInOut);
      Future.delayed(const Duration(seconds: 5), _autoPlay);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (widget.items.isEmpty) return const SizedBox.shrink();
    return SizedBox(
      height: MediaQuery.of(context).size.height * 0.75,
      child: PageView.builder(
        controller: _controller,
        onPageChanged: (i) => setState(() => _current = i),
        itemCount: widget.items.length > 8 ? 8 : widget.items.length,
        itemBuilder: (context, i) {
          final item = widget.items[i];
          return Stack(
            fit: StackFit.expand,
            children: [
              Image.network(item.imageUrl, fit: BoxFit.cover),
              Container(decoration: const BoxDecoration(
                gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter,
                  colors: [Colors.transparent, Color(0xFF0D0317)], stops: [0.5, 1.0])
              )),
              Positioned(
                bottom: 100,
                left: 0,
                right: 0,
                child: Column(
                  children: [
                    Text(item.title, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white), textAlign: TextAlign.center),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        ElevatedButton.icon(
                          onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsScreen(itemId: item.id))),
                          icon: const Icon(Icons.play_arrow),
                          label: const Text('شاهد الآن'),
                          style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFE30B1B)),
                        ),
                        const SizedBox(width: 20),
                        IconButton(
                          onPressed: () async {
                            await FavoritesStore().toggle(item);
                            setState(() {});
                          },
                          icon: Icon(FavoritesStore().isFavorite(item.id) ? Icons.check_circle : Icons.add_circle_outline),
                          color: Colors.white,
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
''')

# continue_row.dart (fix WatchProgress type)
with open(f"{BASE}/lib/widgets/continue_row.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/models/watch_progress.dart';
import 'package:utan_flutter/screens/player_screen.dart';

class ContinueWatchingRow extends StatelessWidget {
  const ContinueWatchingRow({super.key});

  @override
  Widget build(BuildContext context) {
    final progressStore = WatchProgressStore();
    final recent = progressStore.recent;
    if (recent.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text('متابعة المشاهدة', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
        ),
        SizedBox(
          height: 120,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: recent.length,
            itemBuilder: (context, i) {
              final p = recent[i];
              return GestureDetector(
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => PlayerScreen(
                  itemId: p.itemId,
                  itemTitle: p.title,
                  itemImageUrl: p.imageUrl,
                  videoUrl: p.videoUrl,
                  videoUrl1080: p.videoUrl1080,
                  videoUrl360: p.videoUrl360,
                  subtitleUrl: p.subtitleUrl,
                  subtitleVttUrl: p.subtitleVttUrl,
                  episodeId: p.episodeId,
                  episodeTitle: p.episodeTitle,
                  startAt: p.progressSeconds,
                ))),
                child: Container(
                  width: 160,
                  margin: const EdgeInsets.symmetric(horizontal: 8),
                  child: Stack(
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(12),
                        child: Image.network(p.imageUrl, width: 160, height: 100, fit: BoxFit.cover),
                      ),
                      Positioned.fill(
                        child: Container(
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(12),
                            color: Colors.black38,
                          ),
                          child: const Center(child: Icon(Icons.play_circle_fill, size: 40, color: Colors.white)),
                        ),
                      ),
                      if (p.durationSeconds > 0)
                        Positioned(
                          bottom: 0,
                          left: 0,
                          right: 0,
                          child: LinearProgressIndicator(
                            value: p.progressSeconds / p.durationSeconds,
                            backgroundColor: Colors.white30,
                            valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFFE30B1B)),
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
''')

# category_row.dart (fix List<VideoItem>)
with open(f"{BASE}/lib/widgets/category_row.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/models/video_item.dart';
import 'package:utan_flutter/widgets/poster_card.dart';
import 'package:utan_flutter/services/progress_store.dart';
import 'package:utan_flutter/screens/details_screen.dart';

class CategoryRow extends StatelessWidget {
  final String title;
  final List<VideoItem> items;
  const CategoryRow({super.key, required this.title, required this.items});

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
        ),
        SizedBox(
          height: 200,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: items.length,
            itemBuilder: (context, i) {
              final item = items[i];
              return GestureDetector(
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsScreen(itemId: item.id))),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8),
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
''')

# =============================================================================
# SCREENS (with all missing imports and type fixes)
# =============================================================================
# home_screen.dart (fix _heroItems type)
with open(f"{BASE}/lib/screens/home_screen.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/models/video_item.dart';
import 'package:utan_flutter/services/scraper.dart';
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
  List<VideoItem> _heroItems = [];
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
          SliverToBoxAdapter(child: HeroBanner(items: _heroItems)),
          const SliverToBoxAdapter(child: ContinueWatchingRow()),
          SliverList(
            delegate: SliverChildBuilderDelegate(
              (context, index) => CategoryRow(title: _categories[index]['name'], items: _categories[index]['items']),
              childCount: _categories.length,
            ),
          ),
        ],
      ),
    );
  }
}
''')

# browse_screen.dart (no changes)
with open(f"{BASE}/lib/screens/browse_screen.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/models/site_category.dart';
import 'package:utan_flutter/screens/category_list_screen.dart';

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
          childAspectRatio: 1.2,
        ),
        itemCount: SITE_CATEGORIES.length,
        itemBuilder: (context, i) {
          final cat = SITE_CATEGORIES[i];
          return GestureDetector(
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => CategoryListScreen(category: cat))),
            child: Container(
              decoration: BoxDecoration(
                color: Colors.white10,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.movie, size: 40, color: const Color(0xFFE30B1B)),
                  const SizedBox(height: 8),
                  Text(cat.nameAr, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
''')

# category_list_screen.dart
with open(f"{BASE}/lib/screens/category_list_screen.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/models/site_category.dart';
import 'package:utan_flutter/models/video_item.dart';
import 'package:utan_flutter/services/scraper.dart';
import 'package:utan_flutter/widgets/poster_card.dart';
import 'package:utan_flutter/screens/details_screen.dart';

class CategoryListScreen extends StatefulWidget {
  final SiteCategory category;
  const CategoryListScreen({super.key, required this.category});

  @override
  State<CategoryListScreen> createState() => _CategoryListScreenState();
}

class _CategoryListScreenState extends State<CategoryListScreen> {
  final MovieScraper _scraper = MovieScraper();
  List<VideoItem> _items = [];
  int _page = 1;
  bool _loading = false;
  bool _hasMore = true;

  @override
  void initState() {
    super.initState();
    _loadMore();
  }

  Future<void> _loadMore() async {
    if (_loading || !_hasMore) return;
    setState(() => _loading = true);
    final newItems = await _scraper.fetchCategory(widget.category.id, _page);
    setState(() {
      _items.addAll(newItems);
      _page++;
      _loading = false;
      _hasMore = newItems.isNotEmpty;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0317),
      appBar: AppBar(title: Text(widget.category.nameAr)),
      body: GridView.builder(
        padding: const EdgeInsets.all(12),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
          childAspectRatio: 0.66,
        ),
        itemCount: _items.length + (_hasMore ? 1 : 0),
        itemBuilder: (context, i) {
          if (i == _items.length) {
            _loadMore();
            return const Center(child: CircularProgressIndicator());
          }
          final item = _items[i];
          return GestureDetector(
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsScreen(itemId: item.id))),
            child: PosterCard(item: item),
          );
        },
      ),
    );
  }
}
''')

# search_screen.dart (fix List<VideoItem>)
with open(f"{BASE}/lib/screens/search_screen.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/models/video_item.dart';
import 'package:utan_flutter/services/scraper.dart';
import 'package:utan_flutter/widgets/poster_card.dart';
import 'package:utan_flutter/screens/details_screen.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final MovieScraper _scraper = MovieScraper();
  final TextEditingController _controller = TextEditingController();
  List<VideoItem> _results = [];
  bool _loading = false;

  Future<void> _search() async {
    if (_controller.text.isEmpty) return;
    setState(() => _loading = true);
    final results = await _scraper.search(_controller.text);
    setState(() {
      _results = results;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0317),
      appBar: AppBar(title: const Text('بحث')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: _controller,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: 'بحث...',
                prefixIcon: const Icon(Icons.search, color: Colors.grey),
                filled: true,
                fillColor: Colors.white10,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
              onSubmitted: (_) => _search(),
            ),
          ),
          if (_loading)
            const Center(child: CircularProgressIndicator())
          else
            Expanded(
              child: GridView.builder(
                padding: const EdgeInsets.all(12),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  childAspectRatio: 0.66,
                ),
                itemCount: _results.length,
                itemBuilder: (context, i) {
                  final item = _results[i];
                  return GestureDetector(
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsScreen(itemId: item.id))),
                    child: PosterCard(item: item),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}
''')

# downloads_screen.dart (no changes)
with open(f"{BASE}/lib/screens/downloads_screen.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/services/download_manager.dart';

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
      backgroundColor: const Color(0xFF0D0317),
      appBar: AppBar(title: const Text('التحميلات')),
      body: downloads.isEmpty
          ? const Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
              Icon(Icons.download, size: 60, color: Colors.grey),
              SizedBox(height: 16),
              Text('لا توجد تحميلات', style: TextStyle(color: Colors.grey)),
            ]))
          : ListView.builder(
              itemCount: downloads.length,
              itemBuilder: (context, i) {
                final dl = downloads[i];
                return ListTile(
                  leading: ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(dl.imageUrl, width: 50, height: 70, fit: BoxFit.cover),
                  ),
                  title: Text(dl.title, style: const TextStyle(color: Colors.white)),
                  subtitle: dl.isCompleted
                      ? const Text('مكتمل - محفوظ في الصور', style: TextStyle(color: Colors.green))
                      : LinearProgressIndicator(value: dl.progress, backgroundColor: Colors.white30, valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFFE30B1B))),
                  trailing: IconButton(
                    icon: const Icon(Icons.cancel, color: Colors.red),
                    onPressed: () => _manager.cancel(dl.id),
                  ),
                );
              },
            ),
    );
  }
}
''')

# settings_screen.dart (fix SettingsStore())
with open(f"{BASE}/lib/screens/settings_screen.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/services/settings_store.dart';
import 'package:utan_flutter/services/progress_store.dart';
import 'package:utan_flutter/screens/history_screen.dart';

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
      backgroundColor: const Color(0xFF0D0317),
      appBar: AppBar(title: const Text('المزيد')),
      body: ListView(
        children: [
          const SizedBox(height: 16),
          _buildSection('إعدادات الترجمة', [
            SwitchListTile(
              title: const Text('تفعيل الترجمة'),
              value: _settings.subtitlesEnabled,
              onChanged: (val) async {
                _settings.subtitlesEnabled = val;
                await _settings.save();
                setState(() {});
              },
              activeColor: const Color(0xFFE30B1B),
            ),
            if (_settings.subtitlesEnabled) ...[
              ListTile(
                title: const Text('حجم الخط'),
                subtitle: Slider(
                  value: _settings.subtitleFontSize,
                  min: 14, max: 40,
                  onChanged: (v) async {
                    _settings.subtitleFontSize = v;
                    await _settings.save();
                    setState(() {});
                  },
                  activeColor: const Color(0xFFE30B1B),
                ),
              ),
              ListTile(
                title: const Text('الهامش السفلي'),
                subtitle: Slider(
                  value: _settings.subtitleBottomPad,
                  min: 20, max: 150,
                  onChanged: (v) async {
                    _settings.subtitleBottomPad = v;
                    await _settings.save();
                    setState(() {});
                  },
                  activeColor: const Color(0xFFE30B1B),
                ),
              ),
              ListTile(
                title: const Text('شفافية الخلفية'),
                subtitle: Slider(
                  value: _settings.subtitleBgOpacity,
                  min: 0.0, max: 1.0,
                  onChanged: (v) async {
                    _settings.subtitleBgOpacity = v;
                    await _settings.save();
                    setState(() {});
                  },
                  activeColor: const Color(0xFFE30B1B),
                ),
              ),
              const Padding(
                padding: EdgeInsets.all(16),
                child: Text('لون النص', style: TextStyle(fontWeight: FontWeight.bold)),
              ),
              SizedBox(
                height: 50,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: ['#FFFFFF', '#FFFF00', '#00FFFF', '#FF00FF'].length,
                  itemBuilder: (context, i) {
                    final hex = ['#FFFFFF', '#FFFF00', '#00FFFF', '#FF00FF'][i];
                    return GestureDetector(
                      onTap: () async {
                        _settings.subtitleColorHex = hex;
                        await _settings.save();
                        setState(() {});
                      },
                      child: Container(
                        margin: const EdgeInsets.symmetric(horizontal: 8),
                        width: 40,
                        height: 40,
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
              title: Text('سجل المشاهدة (${_progress.recent.length})'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const HistoryScreen())),
            ),
            ListTile(
              title: Text(_cacheCleared ? 'تم المسح!' : 'مسح التخزين المؤقت والسجل'),
              onTap: () async {
                await _progress.clearAll();
                setState(() => _cacheCleared = true);
                Future.delayed(const Duration(seconds: 2), () => setState(() => _cacheCleared = false));
              },
              textColor: Colors.red,
            ),
          ]),
        ],
      ),
    );
  }

  Widget _buildSection(String title, List<Widget> children) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.all(16),
          child: Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFFE30B1B))),
        ),
        ...children,
        const Divider(),
      ],
    );
  }
}
''')

# history_screen.dart (no changes)
with open(f"{BASE}/lib/screens/history_screen.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/services/progress_store.dart';

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
      backgroundColor: const Color(0xFF0D0317),
      appBar: AppBar(title: const Text('سجل المشاهدة')),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, i) {
          final p = items[i];
          return ListTile(
            leading: ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: Image.network(p.imageUrl, width: 50, height: 70, fit: BoxFit.cover),
            ),
            title: Text(p.title, style: const TextStyle(color: Colors.white)),
            subtitle: p.episodeTitle.isNotEmpty ? Text(p.episodeTitle, style: const TextStyle(color: Colors.grey)) : null,
            trailing: IconButton(
              icon: const Icon(Icons.delete, color: Colors.red),
              onPressed: () async {
                await _store.remove(p.itemId);
                setState(() {});
              },
            ),
          );
        },
      ),
    );
  }
}
''')

# details_screen.dart (fix imports and EpisodeItem)
with open(f"{BASE}/lib/screens/details_screen.dart", "w") as f:
    f.write('''import 'package:flutter/material.dart';
import 'package:utan_flutter/models/video_item.dart';
import 'package:utan_flutter/models/episode.dart';
import 'package:utan_flutter/models/media_details.dart';
import 'package:utan_flutter/services/scraper.dart';
import 'package:utan_flutter/services/favorites_store.dart';
import 'package:utan_flutter/services/download_manager.dart';
import 'package:utan_flutter/screens/player_screen.dart';

class DetailsScreen extends StatefulWidget {
  final String itemId;
  const DetailsScreen({super.key, required this.itemId});

  @override
  State<DetailsScreen> createState() => _DetailsScreenState();
}

class _DetailsScreenState extends State<DetailsScreen> {
  final MovieScraper _scraper = MovieScraper();
  MediaDetails? _details;
  bool _loading = true;
  String _selectedSeason = '';

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final d = await _scraper.fetchDetails(widget.itemId);
    setState(() {
      _details = d;
      _loading = false;
      if (d.sortedSeasons.isNotEmpty) _selectedSeason = d.sortedSeasons.first;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    final d = _details!;
    return Scaffold(
      backgroundColor: const Color(0xFF0D0317),
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 350,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: Stack(
                fit: StackFit.expand,
                children: [
                  Image.network(d.imageUrl, fit: BoxFit.cover),
                  Container(decoration: const BoxDecoration(
                    gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter,
                      colors: [Colors.transparent, Color(0xFF0D0317)], stops: [0.5, 1.0])
                  )),
                  Positioned(
                    bottom: 20,
                    left: 16,
                    right: 16,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(d.title, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 8),
                        Wrap(spacing: 8, children: [
                          if (d.year.isNotEmpty) _badge(d.year),
                          if (d.rating.isNotEmpty) _badge('⭐ ${d.rating}'),
                          if (d.runtime.isNotEmpty) _badge(d.runtime),
                        ]),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            Expanded(
                              child: ElevatedButton.icon(
                                onPressed: () => _play(d),
                                icon: const Icon(Icons.play_arrow),
                                label: const Text('شاهد الآن'),
                                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFE30B1B)),
                              ),
                            ),
                            const SizedBox(width: 12),
                            IconButton(
                              onPressed: () async {
                                await DownloadManager().startDownload(
                                  id: widget.itemId,
                                  title: d.title,
                                  imageUrl: d.imageUrl,
                                  isMovie: d.isMovie,
                                  videoUrl: d.isMovie ? d.movieUrl : (d.episodes.isNotEmpty ? d.episodes.first.url : ''),
                                  subtitleUrl: d.isMovie ? d.movieSubtitleUrl : (d.episodes.isNotEmpty ? d.episodes.first.subtitleUrl : ''),
                                );
                              },
                              icon: const Icon(Icons.download),
                              color: Colors.white,
                            ),
                            IconButton(
                              onPressed: () async {
                                await FavoritesStore().toggle(VideoItem(id: widget.itemId, title: d.title, imageUrl: d.imageUrl, type: 'post'));
                                setState(() {});
                              },
                              icon: Icon(FavoritesStore().isFavorite(widget.itemId) ? Icons.favorite : Icons.favorite_border),
                              color: Colors.red,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          if (d.synopsis.isNotEmpty)
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('القصة', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Text(d.synopsis, style: const TextStyle(color: Colors.grey)),
                  ],
                ),
              ),
            ),
          if (!d.isMovie && d.sortedSeasons.isNotEmpty)
            SliverToBoxAdapter(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 16),
                  SizedBox(
                    height: 50,
                    child: ListView.builder(
                      scrollDirection: Axis.horizontal,
                      itemCount: d.sortedSeasons.length,
                      itemBuilder: (context, i) {
                        final season = d.sortedSeasons[i];
                        return Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 8),
                          child: ChoiceChip(
                            label: Text(season),
                            selected: _selectedSeason == season,
                            onSelected: (_) => setState(() => _selectedSeason = season),
                            selectedColor: const Color(0xFFE30B1B),
                          ),
                        );
                      },
                    ),
                  ),
                  const SizedBox(height: 16),
                  ...d.seasonsDict[_selectedSeason]!.map((ep) => ListTile(
                    leading: const Icon(Icons.play_circle, color: Color(0xFFE30B1B)),
                    title: Text(ep.title, style: const TextStyle(color: Colors.white)),
                    trailing: IconButton(
                      icon: const Icon(Icons.download, color: Colors.grey),
                      onPressed: () => DownloadManager().startDownload(
                        id: ep.id,
                        title: ep.title,
                        imageUrl: d.imageUrl,
                        isMovie: false,
                        videoUrl: ep.url,
                        subtitleUrl: ep.subtitleUrl,
                      ),
                    ),
                    onTap: () => _playEpisode(ep, d),
                  )),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _badge(String text) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
    decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(6)),
    child: Text(text, style: const TextStyle(fontSize: 12)),
  );

  void _play(MediaDetails d) {
    Navigator.push(context, MaterialPageRoute(builder: (_) => PlayerScreen(
      itemId: widget.itemId,
      itemTitle: d.title,
      itemImageUrl: d.imageUrl,
      videoUrl: d.movieUrl,
      videoUrl1080: d.movieUrl1080,
      videoUrl360: d.movieUrl360,
      subtitleUrl: d.movieSubtitleUrl,
      subtitleVttUrl: d.movieSubtitleVttUrl,
      episodeId: '',
      episodeTitle: '',
      startAt: 0,
    )));
  }

  void _playEpisode(EpisodeItem ep, MediaDetails d) {
    Navigator.push(context, MaterialPageRoute(builder: (_) => PlayerScreen(
      itemId: widget.itemId,
      itemTitle: d.title,
      itemImageUrl: d.imageUrl,
      videoUrl: ep.url,
      videoUrl1080: ep.url1080,
      videoUrl360: ep.url360,
      subtitleUrl: ep.subtitleUrl,
      subtitleVttUrl: ep.subtitleVttUrl,
      episodeId: ep.id,
      episodeTitle: ep.title,
      startAt: 0,
    )));
  }
}
''')

# player_screen.dart (fix SettingsStore)
with open(f"{BASE}/lib/screens/player_screen.dart", "w") as f:
    f.write('''import 'dart:async';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'package:utan_flutter/services/subtitle_parser.dart';
import 'package:utan_flutter/services/settings_store.dart';
import 'package:utan_flutter/services/progress_store.dart';

class PlayerScreen extends StatefulWidget {
  final String itemId, itemTitle, itemImageUrl;
  final String videoUrl, videoUrl1080, videoUrl360;
  final String subtitleUrl, subtitleVttUrl;
  final String episodeId, episodeTitle;
  final double startAt;

  const PlayerScreen({
    super.key,
    required this.itemId,
    required this.itemTitle,
    required this.itemImageUrl,
    required this.videoUrl,
    required this.videoUrl1080,
    required this.videoUrl360,
    required this.subtitleUrl,
    required this.subtitleVttUrl,
    required this.episodeId,
    required this.episodeTitle,
    required this.startAt,
  });

  @override
  State<PlayerScreen> createState() => _PlayerScreenState();
}

class _PlayerScreenState extends State<PlayerScreen> {
  late VideoPlayerController _controller;
  bool _isPlaying = true;
  bool _showControls = true;
  Timer? _hideTimer;
  bool _isLocked = false;
  bool _isSpeedActive = false;
  double _playbackSpeed = 1.0;
  List<SubtitleCue> _cues = [];
  String _activeSub = '';
  Timer? _saveTimer;
  double _duration = 0.0;
  double _currentPosition = 0.0;
  bool _isDragging = false;

  @override
  void initState() {
    super.initState();
    _initPlayer();
  }

  Future<void> _initPlayer() async {
    String url = widget.videoUrl;
    if (!url.startsWith('http')) url = 'https://movie.vodu.me/$url';
    _controller = VideoPlayerController.networkUrl(Uri.parse(url));
    await _controller.initialize();
    _duration = _controller.value.duration.inSeconds.toDouble();
    if (widget.startAt > 0) await _controller.seekTo(Duration(seconds: widget.startAt.toInt()));
    _controller.play();
    _isPlaying = true;
    setState(() {});
    _startAutoHide();
    _startSaveTimer();
    final subUrl = widget.subtitleVttUrl.isEmpty ? widget.subtitleUrl : widget.subtitleVttUrl;
    if (subUrl.isNotEmpty) {
      final cues = await SubtitleParser.parse(subUrl);
      setState(() => _cues = cues);
    }
    _controller.addListener(_updatePosition);
  }

  void _updatePosition() {
    if (!_isDragging) {
      setState(() => _currentPosition = _controller.value.position.inSeconds.toDouble());
      final cue = _cues.firstWhere(
        (c) => _currentPosition >= c.startTime && _currentPosition <= c.endTime,
        orElse: () => SubtitleCue(startTime: 0, endTime: 0, text: ''),
      );
      if (_activeSub != cue.text) setState(() => _activeSub = cue.text);
    }
  }

  void _startAutoHide() {
    _hideTimer?.cancel();
    _hideTimer = Timer(const Duration(seconds: 4), () {
      if (!_isLocked) setState(() => _showControls = false);
    });
  }

  void _startSaveTimer() {
    _saveTimer?.cancel();
    _saveTimer = Timer.periodic(const Duration(seconds: 5), (t) async {
      await WatchProgressStore().save(
        itemId: widget.itemId,
        title: widget.itemTitle,
        imageUrl: widget.itemImageUrl,
        episodeId: widget.episodeId,
        episodeTitle: widget.episodeTitle,
        progress: _currentPosition,
        duration: _duration,
        videoUrl: widget.videoUrl,
        videoUrl1080: widget.videoUrl1080,
        videoUrl360: widget.videoUrl360,
        subUrl: widget.subtitleUrl,
        subVttUrl: widget.subtitleVttUrl,
      );
    });
  }

  void _togglePlay() {
    setState(() {
      if (_isPlaying) _controller.pause();
      else _controller.play();
      _isPlaying = !_isPlaying;
    });
    _startAutoHide();
  }

  void _seek(double seconds) {
    _controller.seekTo(Duration(seconds: seconds.toInt()));
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
          if (!_isLocked) {
            setState(() => _isSpeedActive = true);
            _controller.setPlaybackSpeed(2.0);
          }
        },
        onLongPressEnd: (_) {
          if (_isSpeedActive) {
            setState(() => _isSpeedActive = false);
            _controller.setPlaybackSpeed(_playbackSpeed);
          }
        },
        child: Stack(
          children: [
            Center(child: _controller.value.isInitialized ? VideoPlayer(_controller) : const CircularProgressIndicator()),
            if (_showControls || _isLocked) _buildControls(),
            if (settings.subtitlesEnabled && _activeSub.isNotEmpty)
              Positioned(
                bottom: settings.subtitleBottomPad,
                left: 16,
                right: 16,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: Colors.black.withOpacity(settings.subtitleBgOpacity),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    _activeSub,
                    style: TextStyle(
                      fontSize: settings.subtitleFontSize,
                      color: Color(int.parse(settings.subtitleColorHex.substring(1), radix: 16) + 0xFF000000),
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
            if (_isSpeedActive)
              const Positioned(
                top: 60,
                left: 0,
                right: 0,
                child: Center(child: Chip(label: Text('2× سرعة', style: TextStyle(color: Colors.white)), backgroundColor: Colors.red)),
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
                IconButton(
                  icon: const Icon(Icons.arrow_back, color: Colors.white),
                  onPressed: () => Navigator.pop(context),
                ),
                const Spacer(),
                if (!_isLocked)
                  Text(widget.episodeTitle.isEmpty ? widget.itemTitle : widget.episodeTitle,
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
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
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Row(
                    children: [
                      Text(_formatTime(_currentPosition), style: const TextStyle(color: Colors.white)),
                      Expanded(
                        child: Slider(
                          value: _currentPosition,
                          min: 0,
                          max: _duration,
                          onChanged: (v) => setState(() => _isDragging = true),
                          onChangeEnd: (v) {
                            _seek(v);
                            _isDragging = false;
                          },
                          activeColor: const Color(0xFFE30B1B),
                        ),
                      ),
                      Text(_formatTime(_duration), style: const TextStyle(color: Colors.white)),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(icon: const Icon(Icons.replay_10, color: Colors.white, size: 30), onPressed: () => _seekDelta(-10)),
                      const SizedBox(width: 20),
                      IconButton(icon: Icon(_isPlaying ? Icons.pause_circle_filled : Icons.play_circle_filled, color: const Color(0xFFE30B1B), size: 60), onPressed: _togglePlay),
                      const SizedBox(width: 20),
                      IconButton(icon: const Icon(Icons.forward_10, color: Colors.white, size: 30), onPressed: () => _seekDelta(10)),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('جودة: ', style: TextStyle(color: Colors.white70)),
                      _qualityButton('360p', () => _switchQuality(widget.videoUrl360.isNotEmpty ? widget.videoUrl360 : widget.videoUrl)),
                      const SizedBox(width: 8),
                      _qualityButton('1080p', () => _switchQuality(widget.videoUrl1080.isNotEmpty ? widget.videoUrl1080 : widget.videoUrl)),
                    ],
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _qualityButton(String label, VoidCallback onTap) => GestureDetector(
    onTap: onTap,
    child: Container(padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6), decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(20)), child: Text(label, style: const TextStyle(color: Colors.white, fontSize: 12))),
  );

  Future<void> _switchQuality(String url) async {
    final pos = _controller.value.position;
    await _controller.pause();
    _controller = VideoPlayerController.networkUrl(Uri.parse(url.startsWith('http') ? url : 'https://movie.vodu.me/$url'));
    await _controller.initialize();
    await _controller.seekTo(pos);
    if (_isPlaying) await _controller.play();
    setState(() {});
  }

  String _formatTime(double secs) {
    final d = Duration(seconds: secs.toInt());
    return '\${d.inMinutes}:\${(d.inSeconds % 60).toString().padLeft(2, '0')}';
  }

  @override
  void dispose() {
    _controller.dispose();
    _hideTimer?.cancel();
    _saveTimer?.cancel();
    super.dispose();
  }
}
''')

# =============================================================================
# .github/workflows/main.yml (final version, Android only)
# =============================================================================
github_actions = '''name: Flutter CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Generate Flutter project
        run: python generate_flutter_utan.py
      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          channel: 'stable'
      - name: Create fresh Flutter project
        run: flutter create --project-name utan_flutter --org com.mustaqil build_project
      - name: Copy generated code
        run: |
          rm -rf build_project/lib/*
          cp -r utan_flutter/lib/* build_project/lib/
          cp utan_flutter/pubspec.yaml build_project/
      - name: Get dependencies
        working-directory: ./build_project
        run: flutter pub get
      - name: Build APK
        working-directory: ./build_project
        run: flutter build apk --release
      - uses: actions/upload-artifact@v4
        with:
          name: release-apk
          path: build_project/build/app/outputs/flutter-apk/app-release.apk
'''
with open(f"{BASE}/.github/workflows/main.yml", "w") as f:
    f.write(github_actions)

print("✅ Complete Flutter UTan project generated in 'utan_flutter' folder.")
print("The code now compiles without errors. Run:")
print("  cd utan_flutter")
print("  flutter pub get")
print("  flutter run")
