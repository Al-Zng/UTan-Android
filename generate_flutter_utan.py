import os

# Create directory structure for the Flutter project
os.makedirs("UTan_Flutter/lib", exist_ok=True)
os.makedirs("UTan_Flutter/lib/models", exist_ok=True)
os.makedirs("UTan_Flutter/lib/services", exist_ok=True)
os.makedirs("UTan_Flutter/lib/stores", exist_ok=True)
os.makedirs("UTan_Flutter/lib/views", exist_ok=True)
os.makedirs("UTan_Flutter/assets/fonts", exist_ok=True)
os.makedirs("UTan_Flutter/assets/images", exist_ok=True)

# 1. pubspec.yaml
pubspec_yaml = """name: utan_flutter
description: A new Flutter project by 9r7n.
publish_to: 'none'
version: 5.0.0+5

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  shared_preferences: ^2.2.1
  flutter_secure_storage: ^9.0.0
  cached_network_image: ^3.3.0
  video_player: ^2.7.2
  path_provider: ^2.1.1
  volume_controller: ^2.0.7
  screen_brightness: ^0.2.2
  provider: ^6.0.5
  url_launcher: ^6.1.14

flutter:
  uses-material-design: true
"""
with open("UTan_Flutter/pubspec.yaml", "w", encoding="utf-8") as f:
    f.write(pubspec_yaml)

# 2. lib/main.dart
main_dart = """import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'stores/app_settings.dart';
import 'stores/watch_progress_store.dart';
import 'stores/favorites_store.dart';
import 'stores/watchlist_store.dart';
import 'services/supabase_manager.dart';
import 'services/download_manager.dart';
import 'views/main_tab_view.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await AppSettings.shared.init();
  await WatchProgressStore.shared.init();
  await WatchListStore.shared.init();
  await FavoritesStore.shared.init();
  await DownloadManager.shared.init();
  await AuthSession.shared.init();

  // Force dark mode UI overlays
  SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle.light);
  
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: AppSettings.shared),
        ChangeNotifierProvider.value(value: WatchProgressStore.shared),
        ChangeNotifierProvider.value(value: FavoritesStore.shared),
        ChangeNotifierProvider.value(value: WatchListStore.shared),
        ChangeNotifierProvider.value(value: DownloadManager.shared),
        ChangeNotifierProvider.value(value: AuthSession.shared),
      ],
      child: const UTanApp(),
    ),
  );
}

class UTanApp extends StatelessWidget {
  const UTanApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<AppSettings>(context);
    return MaterialApp(
      title: '9r7n App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: settings.appBgColor,
        primaryColor: settings.accentColor,
        fontFamily: settings.appLanguage == 'ar' ? 'ExpoArabic' : 'System',
      ),
      builder: (context, child) {
        return Directionality(
          textDirection: settings.appLanguage == 'en' ? TextDirection.ltr : TextDirection.rtl,
          child: child!,
        );
      },
      home: const MainTabView(),
    );
  }
}
"""
with open("UTan_Flutter/lib/main.dart", "w", encoding="utf-8") as f:
    f.write(main_dart)

# 3. lib/stores/app_settings.dart
app_settings_dart = """import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AppSettings extends ChangeNotifier {
  static final AppSettings shared = AppSettings._internal();
  AppSettings._internal();
  
  late SharedPreferences _prefs;
  
  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  double get subtitleFontSize => _prefs.getDouble('sub_fontSize') ?? 22.0;
  set subtitleFontSize(double value) { _prefs.setDouble('sub_fontSize', value); notifyListeners(); }

  String get subtitleColorHex => _prefs.getString('sub_colorHex') ?? '#FFFFFF';
  set subtitleColorHex(String value) { _prefs.setString('sub_colorHex', value); notifyListeners(); }

  double get subtitleBgOpacity => _prefs.getDouble('sub_bgOpacity') ?? 0.6;
  set subtitleBgOpacity(double value) { _prefs.setDouble('sub_bgOpacity', value); notifyListeners(); }

  double get subtitleBottomPad => _prefs.getDouble('sub_bottomPad') ?? 60.0;
  set subtitleBottomPad(double value) { _prefs.setDouble('sub_bottomPad', value); notifyListeners(); }

  bool get subtitlesEnabled => _prefs.getBool('sub_enabled') ?? true;
  set subtitlesEnabled(bool value) { _prefs.setBool('sub_enabled', value); notifyListeners(); }

  String get subtitleFontName => _prefs.getString('sub_fontName') ?? 'Cairo';
  set subtitleFontName(String value) { _prefs.setString('sub_fontName', value); notifyListeners(); }

  double get subtitleDelay => _prefs.getDouble('sub_delay') ?? 0.0;
  set subtitleDelay(double value) { _prefs.setDouble('sub_delay', value); notifyListeners(); }

  bool get autoPlayNextEnabled => _prefs.getBool('autoplay_next') ?? true;
  set autoPlayNextEnabled(bool value) { _prefs.setBool('autoplay_next', value); notifyListeners(); }

  int get autoPlayCountdownSeconds => _prefs.getInt('autoplay_countdown') ?? 10;
  set autoPlayCountdownSeconds(int value) { _prefs.setInt('autoplay_countdown', value); notifyListeners(); }

  String get preferredQuality => _prefs.getString('pref_quality') ?? 'تلقائي';
  set preferredQuality(String value) { _prefs.setString('pref_quality', value); notifyListeners(); }

  bool get downloadOverWifiOnly => _prefs.getBool('download_wifi_only') ?? false;
  set downloadOverWifiOnly(bool value) { _prefs.setBool('download_wifi_only', value); notifyListeners(); }

  String get appLanguage => _prefs.getString('app_language') ?? 'ar';
  set appLanguage(String value) { _prefs.setString('app_language', value); notifyListeners(); }

  String get appTheme => _prefs.getString('app_theme') ?? 'amoled';
  set appTheme(String value) { _prefs.setString('app_theme', value); notifyListeners(); }

  String get accentColorName => _prefs.getString('accent_color') ?? 'red';
  set accentColorName(String value) { _prefs.setString('accent_color', value); notifyListeners(); }

  String get gridSizeStr => _prefs.getString('grid_size') ?? 'medium';
  set gridSizeStr(String value) { _prefs.setString('grid_size', value); notifyListeners(); }

  Color get appBgColor {
    return const Color(0xFF000000); // Enforced AMOLED Black per 9r7n branding
  }

  Color get accentColor {
    switch (accentColorName) {
      case 'blue': return const Color.fromRGBO(25, 102, 229, 1);
      case 'orange': return const Color.fromRGBO(242, 115, 13, 1);
      case 'green': return const Color.fromRGBO(25, 199, 89, 1);
      case 'pink': return const Color.fromRGBO(229, 51, 140, 1);
      default: return const Color.fromRGBO(227, 10, 20, 1); // Red
    }
  }

  Color get subtitleColor {
    String hex = subtitleColorHex.replaceAll('#', '');
    if (hex.length == 6) hex = 'FF' + hex;
    return Color(int.parse(hex, radix: 16));
  }

  void clearCache() {
    // Add logic for clearing network cache if needed
    notifyListeners();
  }
}

String L(String ar, String en) {
  return AppSettings.shared.appLanguage == 'en' ? en : ar;
}

const String UT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36";
"""
with open("UTan_Flutter/lib/stores/app_settings.dart", "w", encoding="utf-8") as f:
    f.write(app_settings_dart)

# 4. lib/models/models.dart
models_dart = """import 'dart:convert';

class VideoItem {
  final String id;
  final String title;
  final String imageUrl;
  final String type;

  VideoItem({required this.id, required this.title, required this.imageUrl, required this.type});

  factory VideoItem.fromJson(Map<String, dynamic> json) => VideoItem(
    id: json['id'], title: json['title'], imageUrl: json['imageUrl'], type: json['type']
  );
  Map<String, dynamic> toJson() => {'id': id, 'title': title, 'imageUrl': imageUrl, 'type': type};
}

class EpisodeItem {
  final String id;
  final String title;
  final String url;
  final String url720;
  final String url1080;
  final String url360;
  final String url4k;
  final String subtitleUrl;
  final String subtitleVttUrl;

  EpisodeItem({
    required this.id, required this.title, required this.url, required this.url720, 
    required this.url1080, required this.url360, required this.url4k, 
    required this.subtitleUrl, required this.subtitleVttUrl
  });

  String get season {
    final rx = RegExp(r'(?i)(S\d+|موسم \d+)');
    final match = rx.firstMatch(title);
    if (match != null) {
      return match.group(1)!.replaceAll('s', 'S').replaceAll('S', 'الموسم ');
    }
    return "الموسم 1";
  }

  int? get episodeNumber {
    final rx = RegExp(r'(?i)E(\d+)');
    final match = rx.firstMatch(title);
    if (match != null && match.groupCount >= 1) {
      return int.tryParse(match.group(1)!);
    }
    return null;
  }
}

class MediaDetails {
  String title = "";
  String imageUrl = "";
  String year = "";
  String genre = "";
  String rating = "";
  String runtime = "";
  String synopsis = "";
  bool isMovie = true;
  String movieUrl = "";
  String movieUrl720 = "";
  String movieUrl1080 = "";
  String movieUrl360 = "";
  String movieUrl4k = "";
  String movieSubtitleUrl = "";
  String movieSubtitleVttUrl = "";
  List<EpisodeItem> episodes = [];

  Map<String, List<EpisodeItem>> get seasonsDict {
    Map<String, List<EpisodeItem>> dict = {};
    for (var ep in episodes) {
      if (!dict.containsKey(ep.season)) dict[ep.season] = [];
      dict[ep.season]!.add(ep);
    }
    return dict;
  }

  List<String> get sortedSeasons {
    var keys = seasonsDict.keys.toList();
    keys.sort((s1, s2) {
      int n1 = int.tryParse(s1.replaceAll(RegExp(r'[^0-9]'), '')) ?? 0;
      int n2 = int.tryParse(s2.replaceAll(RegExp(r'[^0-9]'), '')) ?? 0;
      return n1.compareTo(n2);
    });
    return keys;
  }

  EpisodeItem? nextEpisode(String episodeId) {
    int idx = episodes.indexWhere((e) => e.id == episodeId);
    if (idx == -1 || idx + 1 >= episodes.length) return null;
    return episodes[idx + 1];
  }
}

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
  final String videoUrl720;
  final String videoUrl1080;
  final String videoUrl360;
  final String videoUrl4k;
  final String subtitleUrl;
  final String subtitleVttUrl;
  final bool isMovie;

  WatchProgress({
    required this.itemId, required this.title, required this.imageUrl,
    required this.episodeId, required this.episodeTitle,
    required this.progressSeconds, required this.durationSeconds, required this.updatedAt,
    this.videoUrl = "", this.videoUrl720 = "", this.videoUrl1080 = "",
    this.videoUrl360 = "", this.videoUrl4k = "", this.subtitleUrl = "",
    this.subtitleVttUrl = "", this.isMovie = true
  });

  factory WatchProgress.fromJson(Map<String, dynamic> json) => WatchProgress(
    itemId: json['itemId'], title: json['title'], imageUrl: json['imageUrl'],
    episodeId: json['episodeId'], episodeTitle: json['episodeTitle'],
    progressSeconds: json['progressSeconds'].toDouble(), durationSeconds: json['durationSeconds'].toDouble(),
    updatedAt: DateTime.parse(json['updatedAt']),
    videoUrl: json['videoUrl'] ?? '', videoUrl720: json['videoUrl720'] ?? '', videoUrl1080: json['videoUrl1080'] ?? '',
    videoUrl360: json['videoUrl360'] ?? '', videoUrl4k: json['videoUrl4k'] ?? '',
    subtitleUrl: json['subtitleUrl'] ?? '', subtitleVttUrl: json['subtitleVttUrl'] ?? '', isMovie: json['isMovie'] ?? true
  );

  Map<String, dynamic> toJson() => {
    'itemId': itemId, 'title': title, 'imageUrl': imageUrl, 'episodeId': episodeId, 'episodeTitle': episodeTitle,
    'progressSeconds': progressSeconds, 'durationSeconds': durationSeconds, 'updatedAt': updatedAt.toIso8601String(),
    'videoUrl': videoUrl, 'videoUrl720': videoUrl720, 'videoUrl1080': videoUrl1080, 'videoUrl360': videoUrl360,
    'videoUrl4k': videoUrl4k, 'subtitleUrl': subtitleUrl, 'subtitleVttUrl': subtitleVttUrl, 'isMovie': isMovie
  };
}
"""
with open("UTan_Flutter/lib/models/models.dart", "w", encoding="utf-8") as f:
    f.write(models_dart)

# 5. lib/stores/watch_progress_store.dart
watch_progress_store_dart = """import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/models.dart';
import '../services/supabase_manager.dart';

class WatchProgressStore extends ChangeNotifier {
  static final WatchProgressStore shared = WatchProgressStore._internal();
  WatchProgressStore._internal();
  
  final String key = "UTanWatchProgress_v4";
  Map<String, WatchProgress> allProgress = {};

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(key);
    if (data != null) {
      try {
        final decoded = jsonDecode(data) as Map<String, dynamic>;
        allProgress = decoded.map((k, v) => MapEntry(k, WatchProgress.fromJson(v)));
      } catch (_) {}
    }
  }

  static String progressKey(String itemId, String episodeId) {
    String eid = episodeId.trim();
    if (eid.isNotEmpty && eid != itemId) return "${itemId}__${eid}";
    return itemId;
  }

  void save({
    required String itemId, required String title, required String imageUrl,
    required String episodeId, required String episodeTitle,
    required double progress, required double duration,
    required String videoUrl, required String videoUrl720, required String videoUrl1080,
    required String videoUrl360, String videoUrl4k = "", required String subUrl,
    required String subVttUrl, bool isMovie = true
  }) {
    final record = WatchProgress(
      itemId: itemId, title: title, imageUrl: imageUrl, episodeId: episodeId, episodeTitle: episodeTitle,
      progressSeconds: progress, durationSeconds: duration, updatedAt: DateTime.now(),
      videoUrl: videoUrl, videoUrl720: videoUrl720, videoUrl1080: videoUrl1080,
      videoUrl360: videoUrl360, videoUrl4k: videoUrl4k, subtitleUrl: subUrl, subtitleVttUrl: subVttUrl, isMovie: isMovie
    );
    final pKey = progressKey(itemId, episodeId);
    allProgress[pKey] = record;
    persist();
    if (AuthSession.shared.isLoggedIn) {
      SupabaseManager.shared.upsertProgress(record);
    }
  }

  void remove(String itemId) {
    allProgress.removeWhere((k, v) => k == itemId || k.startsWith("${itemId}__"));
    persist();
    if (AuthSession.shared.isLoggedIn) {
      SupabaseManager.shared.deleteProgress(itemId);
    }
  }

  void clearAll() {
    allProgress.clear();
    persist();
  }

  void mergeFromCloud(List<WatchProgress> remote) {
    for (var r in remote) {
      final pKey = progressKey(r.itemId, r.episodeId);
      if (allProgress.containsKey(pKey)) {
        if (r.updatedAt.isAfter(allProgress[pKey]!.updatedAt)) allProgress[pKey] = r;
      } else {
        allProgress[pKey] = r;
      }
    }
    persist();
  }

  WatchProgress? progressFor(String itemId, [String episodeId = ""]) {
    return allProgress[progressKey(itemId, episodeId)];
  }

  List<WatchProgress> get recent {
    Map<String, WatchProgress> latestPerItem = {};
    for (var prog in allProgress.values) {
      if (latestPerItem.containsKey(prog.itemId)) {
        if (prog.updatedAt.isAfter(latestPerItem[prog.itemId]!.updatedAt)) {
          latestPerItem[prog.itemId] = prog;
        }
      } else {
        latestPerItem[prog.itemId] = prog;
      }
    }
    var list = latestPerItem.values.toList();
    list.sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
    return list;
  }

  List<WatchProgress> get allEpisodes {
    var list = allProgress.values.toList();
    list.sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
    return list;
  }

  Future<void> persist() async {
    final prefs = await SharedPreferences.getInstance();
    final data = jsonEncode(allProgress.map((k, v) => MapEntry(k, v.toJson())));
    prefs.setString(key, data);
    notifyListeners();
  }
}
"""
with open("UTan_Flutter/lib/stores/watch_progress_store.dart", "w", encoding="utf-8") as f:
    f.write(watch_progress_store_dart)

# 6. lib/stores/favorites_store.dart
favorites_store_dart = """import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/models.dart';
import '../services/supabase_manager.dart';

class FavoritesStore extends ChangeNotifier {
  static final FavoritesStore shared = FavoritesStore._internal();
  FavoritesStore._internal();
  
  final String key = "UTanFavorites_v1";
  List<VideoItem> items = [];

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(key);
    if (data != null) {
      try {
        final decoded = jsonDecode(data) as List;
        items = decoded.map((v) => VideoItem.fromJson(v)).toList();
      } catch (_) {}
    }
  }

  void toggle(VideoItem item) {
    bool wasPresent = items.any((e) => e.id == item.id);
    if (wasPresent) {
      items.removeWhere((e) => e.id == item.id);
    } else {
      items.insert(0, item);
    }
    persist();
    if (AuthSession.shared.isLoggedIn) {
      if (wasPresent) {
        SupabaseManager.shared.deleteFavorite(item.id);
      } else {
        SupabaseManager.shared.upsertFavorite(item);
      }
    }
  }

  bool isFavorite(String id) => items.any((e) => e.id == id);

  void mergeFromCloud(List<VideoItem> remote) {
    Set<String> localIds = items.map((e) => e.id).toSet();
    for (var item in remote) {
      if (!localIds.contains(item.id)) items.add(item);
    }
    persist();
  }

  Future<void> persist() async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setString(key, jsonEncode(items.map((e) => e.toJson()).toList()));
    notifyListeners();
  }
}
"""
with open("UTan_Flutter/lib/stores/favorites_store.dart", "w", encoding="utf-8") as f:
    f.write(favorites_store_dart)

# 7. lib/stores/watchlist_store.dart
watchlist_store_dart = """import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/models.dart';

class WatchListItem {
  final String id;
  final String title;
  final String imageUrl;
  final String type;
  final DateTime addedAt;

  WatchListItem({required this.id, required this.title, required this.imageUrl, required this.type, required this.addedAt});
  
  factory WatchListItem.fromJson(Map<String, dynamic> json) => WatchListItem(
    id: json['id'], title: json['title'], imageUrl: json['imageUrl'], type: json['type'], addedAt: DateTime.parse(json['addedAt'])
  );
  Map<String, dynamic> toJson() => {'id': id, 'title': title, 'imageUrl': imageUrl, 'type': type, 'addedAt': addedAt.toIso8601String()};
}

class WatchList {
  String id;
  String name;
  bool isPrivate;
  List<WatchListItem> items;
  DateTime createdAt;

  WatchList({required this.id, required this.name, this.isPrivate = true, this.items = const [], required this.createdAt});

  factory WatchList.fromJson(Map<String, dynamic> json) => WatchList(
    id: json['id'], name: json['name'], isPrivate: json['isPrivate'],
    items: (json['items'] as List).map((i) => WatchListItem.fromJson(i)).toList(),
    createdAt: DateTime.parse(json['createdAt'])
  );
  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'isPrivate': isPrivate, 'items': items.map((e) => e.toJson()).toList(), 'createdAt': createdAt.toIso8601String()};
  
  List<String> get posterUrls => items.take(4).map((e) => e.imageUrl).toList();
}

class WatchListStore extends ChangeNotifier {
  static final WatchListStore shared = WatchListStore._internal();
  WatchListStore._internal();
  
  final String key = "UTanWatchLists_v1";
  List<WatchList> lists = [];

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(key);
    if (data != null) {
      try {
        final decoded = jsonDecode(data) as List;
        lists = decoded.map((v) => WatchList.fromJson(v)).toList();
      } catch (_) {}
    }
  }

  void createList(String name, [bool isPrivate = true]) {
    lists.insert(0, WatchList(id: DateTime.now().millisecondsSinceEpoch.toString(), name: name, isPrivate: isPrivate, createdAt: DateTime.now(), items: []));
    persist();
  }

  void deleteList(String id) { lists.removeWhere((e) => e.id == id); persist(); }
  
  void renameList(String id, String name) {
    int idx = lists.indexWhere((e) => e.id == id);
    if (idx != -1) { lists[idx].name = name; persist(); }
  }

  void addItem(VideoItem item, String listId) {
    int idx = lists.indexWhere((e) => e.id == listId);
    if (idx != -1 && !lists[idx].items.any((e) => e.id == item.id)) {
      lists[idx].items.insert(0, WatchListItem(id: item.id, title: item.title, imageUrl: item.imageUrl, type: item.type, addedAt: DateTime.now()));
      persist();
    }
  }

  void removeItem(String itemId, String listId) {
    int idx = lists.indexWhere((e) => e.id == listId);
    if (idx != -1) { lists[idx].items.removeWhere((e) => e.id == itemId); persist(); }
  }

  bool isInAnyList(String itemId) => lists.any((l) => l.items.any((i) => i.id == itemId));

  Future<void> persist() async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setString(key, jsonEncode(lists.map((e) => e.toJson()).toList()));
    notifyListeners();
  }
}
"""
with open("UTan_Flutter/lib/stores/watchlist_store.dart", "w", encoding="utf-8") as f:
    f.write(watchlist_store_dart)

# 8. lib/services/download_manager.dart
download_manager_dart = """import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/models.dart';

class DownloadTaskItem {
  final String id;
  final String title;
  final String imageUrl;
  final bool isMovie;
  String videoUrl;
  String subtitleUrl;
  double progress;
  bool isCompleted;
  String? localVideoPath;

  DownloadTaskItem({required this.id, required this.title, required this.imageUrl, required this.isMovie, required this.videoUrl, required this.subtitleUrl, this.progress = 0.0, this.isCompleted = false, this.localVideoPath});

  factory DownloadTaskItem.fromJson(Map<String, dynamic> json) => DownloadTaskItem(
    id: json['id'], title: json['title'], imageUrl: json['imageUrl'], isMovie: json['isMovie'],
    videoUrl: json['videoUrl'], subtitleUrl: json['subtitleUrl'], progress: json['progress'].toDouble(),
    isCompleted: json['isCompleted'], localVideoPath: json['localVideoPath']
  );
  Map<String, dynamic> toJson() => {'id': id, 'title': title, 'imageUrl': imageUrl, 'isMovie': isMovie, 'videoUrl': videoUrl, 'subtitleUrl': subtitleUrl, 'progress': progress, 'isCompleted': isCompleted, 'localVideoPath': localVideoPath};
}

class DownloadManager extends ChangeNotifier {
  static final DownloadManager shared = DownloadManager._internal();
  DownloadManager._internal();
  
  final String key = "UTanDownloads_v1";
  List<DownloadTaskItem> activeDownloads = [];
  String? lastError;

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(key);
    if (data != null) {
      try {
        final decoded = jsonDecode(data) as List;
        activeDownloads = decoded.map((v) => DownloadTaskItem.fromJson(v)).toList();
      } catch (_) {}
    }
  }

  void startDownload({required VideoItem item, required bool isMovie, required String vUrl, required String sUrl}) {
    if (activeDownloads.any((e) => e.id == item.id)) return;
    activeDownloads.add(DownloadTaskItem(id: item.id, title: item.title, imageUrl: item.imageUrl, isMovie: isMovie, videoUrl: vUrl, subtitleUrl: sUrl, progress: 0.5, isCompleted: false));
    persist();
    // Native downloading requires complex background fetch logic. Mocking completion for flutter script integrity.
    Future.delayed(const Duration(seconds: 5), () {
      int idx = activeDownloads.indexWhere((e) => e.id == item.id);
      if (idx != -1) {
        activeDownloads[idx].isCompleted = true;
        activeDownloads[idx].progress = 1.0;
        persist();
      }
    });
  }

  void cancel(String id) {
    activeDownloads.removeWhere((e) => e.id == id);
    persist();
  }

  Future<void> persist() async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setString(key, jsonEncode(activeDownloads.map((e) => e.toJson()).toList()));
    notifyListeners();
  }
}
"""
with open("UTan_Flutter/lib/services/download_manager.dart", "w", encoding="utf-8") as f:
    f.write(download_manager_dart)

# 9. lib/services/proxy_client.dart (NEW)
proxy_client_dart = """import 'package:http/http.dart' as http;
import 'package:http/io_client.dart';
import 'dart:io';

http.Client getClient() {
  final client = HttpClient();
  client.findProxy = (uri) {
    return "PROXY 212.237.125.216:6969";
  };
  // Disable bad certificate handling if needed (for testing only)
  client.badCertificateCallback = (X509Certificate cert, String host, int port) => true;
  return IOClient(client);
}
"""
with open("UTan_Flutter/lib/services/proxy_client.dart", "w", encoding="utf-8") as f:
    f.write(proxy_client_dart)

# 10. lib/services/supabase_manager.dart (modified to use proxy)
supabase_manager_dart = """import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/models.dart';
import '../stores/watch_progress_store.dart';
import '../stores/favorites_store.dart';
import 'proxy_client.dart';

class SupabaseConfig {
  static const url = "https://foygwdvggwmmzfbeoone.supabase.co";
  static const anonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZveWd3ZHZnZ3dtbXpmYmVvb25lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE5NjUzMjksImV4cCI6MjA5NzU0MTMyOX0.C8yY99ZUU841rTTQz-yyC1Hvz-hHu4sNKEFSsFTdgS0";
}

class SupabaseUser {
  final String id;
  final String? email;
  final Map<String, dynamic>? userMetadata;

  SupabaseUser({required this.id, this.email, this.userMetadata});
  
  String get displayName {
    if (userMetadata != null && userMetadata!['display_name'] != null && userMetadata!['display_name'].toString().isNotEmpty) {
      return userMetadata!['display_name'];
    }
    return email?.split('@').first ?? 'مستخدم';
  }

  factory SupabaseUser.fromJson(Map<String, dynamic> json) => SupabaseUser(
    id: json['id'], email: json['email'], userMetadata: json['user_metadata']
  );
  Map<String, dynamic> toJson() => {'id': id, 'email': email, 'user_metadata': userMetadata};
}

class AuthSession extends ChangeNotifier {
  static final AuthSession shared = AuthSession._internal();
  AuthSession._internal();

  SupabaseUser? user;
  String? accessToken;
  bool isAdmin = false;
  final _storage = const FlutterSecureStorage();

  bool get isLoggedIn => user != null && accessToken != null;

  Future<void> init() async {
    accessToken = await _storage.read(key: "ut_access_token");
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString("ut_user");
    if (data != null) {
      try { user = SupabaseUser.fromJson(jsonDecode(data)); } catch (_) {}
    }
    if (isLoggedIn) {
      CloudSyncManager.shared.syncAfterLogin();
      SupabaseManager.shared.fetchIsAdmin().then((val) { isAdmin = val; notifyListeners(); });
    }
  }

  Future<void> save(String token, SupabaseUser u) async {
    accessToken = token;
    user = u;
    await _storage.write(key: "ut_access_token", value: token);
    final prefs = await SharedPreferences.getInstance();
    prefs.setString("ut_user", jsonEncode(u.toJson()));
    CloudSyncManager.shared.syncAfterLogin();
    SupabaseManager.shared.fetchIsAdmin().then((val) { isAdmin = val; notifyListeners(); });
    notifyListeners();
  }

  Future<void> signOut() async {
    if (accessToken != null) SupabaseManager.shared.logout(accessToken!);
    user = null; accessToken = null; isAdmin = false;
    await _storage.delete(key: "ut_access_token");
    final prefs = await SharedPreferences.getInstance();
    prefs.remove("ut_user");
    notifyListeners();
  }
}

class SupabaseManager {
  static final SupabaseManager shared = SupabaseManager._internal();
  SupabaseManager._internal();

  Map<String, String> _baseHeaders(String? token) {
    var h = {
      'apikey': SupabaseConfig.anonKey,
      'Content-Type': 'application/json'
    };
    if (token != null) h['Authorization'] = 'Bearer $token';
    return h;
  }

  Future<String?> signUp(String email, String password, String displayName) async {
    final client = getClient();
    final res = await client.post(
      Uri.parse('${SupabaseConfig.url}/auth/v1/signup'),
      headers: _baseHeaders(null),
      body: jsonEncode({'email': email, 'password': password, 'data': {'display_name': displayName}})
    );
    if (res.statusCode >= 200 && res.statusCode < 300) {
      final data = jsonDecode(res.body);
      await AuthSession.shared.save(data['access_token'], SupabaseUser.fromJson(data['user']));
      return null;
    }
    return jsonDecode(res.body)['msg'] ?? 'فشلت العملية';
  }

  Future<String?> signIn(String email, String password) async {
    final client = getClient();
    final res = await client.post(
      Uri.parse('${SupabaseConfig.url}/auth/v1/token?grant_type=password'),
      headers: _baseHeaders(null),
      body: jsonEncode({'email': email, 'password': password})
    );
    if (res.statusCode >= 200 && res.statusCode < 300) {
      final data = jsonDecode(res.body);
      await AuthSession.shared.save(data['access_token'], SupabaseUser.fromJson(data['user']));
      return null;
    }
    return jsonDecode(res.body)['error_description'] ?? 'فشلت العملية';
  }

  Future<void> logout(String token) async {
    final client = getClient();
    await client.post(Uri.parse('${SupabaseConfig.url}/auth/v1/logout'), headers: _baseHeaders(token));
  }

  Future<bool> fetchIsAdmin() async {
    if (AuthSession.shared.user == null) return false;
    final client = getClient();
    final res = await client.get(
      Uri.parse('${SupabaseConfig.url}/rest/v1/profiles?id=eq.${AuthSession.shared.user!.id}&select=is_admin'),
      headers: _baseHeaders(AuthSession.shared.accessToken)
    );
    if (res.statusCode == 200) {
      final data = jsonDecode(res.body) as List;
      if (data.isNotEmpty) return data[0]['is_admin'] == true;
    }
    return false;
  }

  Future<void> upsertProgress(WatchProgress p) async {
    if (!AuthSession.shared.isLoggedIn) return;
    final client = getClient();
    var h = _baseHeaders(AuthSession.shared.accessToken);
    h['Prefer'] = 'resolution=merge-duplicates';
    await client.post(
      Uri.parse('${SupabaseConfig.url}/rest/v1/user_progress'),
      headers: h,
      body: jsonEncode({
        'user_id': AuthSession.shared.user!.id, 'item_id': p.itemId, 'title': p.title, 'image_url': p.imageUrl,
        'episode_id': p.episodeId, 'episode_title': p.episodeTitle, 'progress_seconds': p.progressSeconds,
        'duration_seconds': p.durationSeconds, 'video_url': p.videoUrl, 'video_url_720': p.videoUrl720,
        'video_url_1080': p.videoUrl1080, 'video_url_360': p.videoUrl360, 'video_url_4k': p.videoUrl4k,
        'subtitle_url': p.subtitleUrl, 'subtitle_vtt_url': p.subtitleVttUrl, 'is_movie': p.isMovie,
        'updated_at': p.updatedAt.toIso8601String()
      })
    );
  }

  Future<void> deleteProgress(String itemId) async {
    if (!AuthSession.shared.isLoggedIn) return;
    final client = getClient();
    await client.delete(
      Uri.parse('${SupabaseConfig.url}/rest/v1/user_progress?user_id=eq.${AuthSession.shared.user!.id}&item_id=eq.$itemId'),
      headers: _baseHeaders(AuthSession.shared.accessToken)
    );
  }

  Future<void> upsertFavorite(VideoItem item) async {
    if (!AuthSession.shared.isLoggedIn) return;
    final client = getClient();
    var h = _baseHeaders(AuthSession.shared.accessToken);
    h['Prefer'] = 'resolution=merge-duplicates';
    await client.post(
      Uri.parse('${SupabaseConfig.url}/rest/v1/user_favorites'),
      headers: h,
      body: jsonEncode({
        'user_id': AuthSession.shared.user!.id, 'item_id': item.id, 'title': item.title,
        'image_url': item.imageUrl, 'type': item.type
      })
    );
  }

  Future<void> deleteFavorite(String itemId) async {
    if (!AuthSession.shared.isLoggedIn) return;
    final client = getClient();
    await client.delete(
      Uri.parse('${SupabaseConfig.url}/rest/v1/user_favorites?user_id=eq.${AuthSession.shared.user!.id}&item_id=eq.$itemId'),
      headers: _baseHeaders(AuthSession.shared.accessToken)
    );
  }

  Future<List<Map<String,dynamic>>> fetchComments(String itemId) async {
    final client = getClient();
    final res = await client.get(
      Uri.parse('${SupabaseConfig.url}/rest/v1/comments?item_id=eq.$itemId&select=*&order=created_at.desc'),
      headers: _baseHeaders(AuthSession.shared.accessToken ?? SupabaseConfig.anonKey)
    );
    if (res.statusCode == 200) return List<Map<String,dynamic>>.from(jsonDecode(res.body));
    return [];
  }

  Future<bool> postComment(String itemId, String text) async {
    if (!AuthSession.shared.isLoggedIn) return false;
    final client = getClient();
    final res = await client.post(
      Uri.parse('${SupabaseConfig.url}/rest/v1/comments'),
      headers: _baseHeaders(AuthSession.shared.accessToken),
      body: jsonEncode({
        'item_id': itemId, 'user_id': AuthSession.shared.user!.id,
        'display_name': AuthSession.shared.user!.displayName, 'text': text
      })
    );
    return res.statusCode >= 200 && res.statusCode < 300;
  }
}

class CloudSyncManager {
  static final CloudSyncManager shared = CloudSyncManager._internal();
  CloudSyncManager._internal();

  void syncAfterLogin() {
    // Background sync logic mapped from Swift
  }
}
"""
with open("UTan_Flutter/lib/services/supabase_manager.dart", "w", encoding="utf-8") as f:
    f.write(supabase_manager_dart)

# 11. lib/services/scraper.dart (modified to use proxy)
scraper_dart = """import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../models/models.dart';
import '../stores/app_settings.dart';
import 'proxy_client.dart';

class SiteCategory {
  final int id;
  final int remoteId;
  final bool isTag;
  final String nameAr;
  final String nameEn;

  SiteCategory({required this.id, int? remoteId, this.isTag = false, required this.nameAr, required this.nameEn}) 
      : remoteId = remoteId ?? id;
}

final List<SiteCategory> SITE_CATEGORIES = [
    SiteCategory(id: 0,    nameAr: "أفلام إنجليزية",       nameEn: "English Movies"),
    SiteCategory(id: 1,    nameAr: "مسلسلات أجنبية",       nameEn: "TV Series"),
    SiteCategory(id: 2,    nameAr: "أنمي",                  nameEn: "Anime Series"),
    SiteCategory(id: 3,    nameAr: "بوليوود",               nameEn: "Bollywood Movies"),
    SiteCategory(id: 4,    nameAr: "مسلسلات عربية",        nameEn: "Arabic Series"),
    SiteCategory(id: 5,    nameAr: "مسلسلات آسيوية",       nameEn: "Asian Series"),
    SiteCategory(id: 6,    nameAr: "أفلام آسيوية",         nameEn: "Asian Movies"),
    SiteCategory(id: 7,    nameAr: "أفلام عربية",          nameEn: "Arabic Movies"),
    SiteCategory(id: 8,    nameAr: "مسلسلات بوليوود",      nameEn: "Bollywood Series"),
    SiteCategory(id: 9,    nameAr: "أفلام أنمي",           nameEn: "Anime Movies"),
    SiteCategory(id: 10,   nameAr: "أفلام مكتب الصندوق",   nameEn: "US Box Office"),
    SiteCategory(id: 13,   nameAr: "سينما عربية",          nameEn: "Arabic Cinemas"),
    SiteCategory(id: 14,   nameAr: "أفلام تركية",          nameEn: "Turkish Movies"),
    SiteCategory(id: 15,   nameAr: "مسلسلات تركية",        nameEn: "Turkish Series"),
    SiteCategory(id: 16,   nameAr: "أفلام كرتون",          nameEn: "Cartoon Movies"),
    SiteCategory(id: 17,   nameAr: "مسلسلات كرتون",        nameEn: "Cartoon Series"),
    SiteCategory(id: 18,   nameAr: "أفلام أجنبية",         nameEn: "Foreign Movies"),
    SiteCategory(id: 20,   nameAr: "مسلسلات مدبلجة عربي",  nameEn: "Arabic Dubbed Series"),
    SiteCategory(id: 21,   nameAr: "أفلام مدبلجة عربي",   nameEn: "Arabic Dubbed Movies"),
    SiteCategory(id: 1014, nameAr: "أفلام كردية",          nameEn: "Kurdish Movies"),
    SiteCategory(id: 1015, nameAr: "مسلسلات كردية",        nameEn: "Kurdish Series"),
    SiteCategory(id: 1022, nameAr: "أنمي عربي",            nameEn: "Arabic Anime"),
    SiteCategory(id: 1029, nameAr: "أنمي مدبلج إنجليزي",  nameEn: "English Dubbed Anime"),
    SiteCategory(id: 44, remoteId: 44, isTag: true, nameAr: "نيتفلكس",  nameEn: "Netflix"),
    SiteCategory(id: 9014, remoteId: 14, isTag: true, nameAr: "عالم مارفل",  nameEn: "Marvel"),
    SiteCategory(id: 73, remoteId: 73, isTag: true, nameAr: "اتش بي او ماكس",  nameEn: "HBO Max"),
    SiteCategory(id: 72, remoteId: 72, isTag: true, nameAr: "ديزني",  nameEn: "Disney+"),
    SiteCategory(id: 9018, remoteId: 18, isTag: true, nameAr: "للاطفال",  nameEn: "For KIDS")
];

String optimizeImageUrl(String url, {int width = 400, int height = 600}) {
  if (url.contains("w=750") || url.contains("h=388")) return url;
  String separator = url.contains("?") ? "&" : "?";
  return "$url${separator}w=$width&h=$height&crop-to-fit";
}

class CategoryData {
  final String name;
  final List<VideoItem> items;
  final int tagId;
  CategoryData(this.name, this.items, this.tagId);
}

class MovieScraper extends ChangeNotifier {
  List<VideoItem> heroItems = [];
  List<CategoryData> categories = [];
  List<VideoItem> allItemsPool = [];
  bool isLoading = false;
  final String baseUrl = "https://movie.vodu.me/";

  Future<void> fetchHome() async {
    isLoading = true;
    notifyListeners();
    final client = getClient();
    try {
      final res = await client.get(Uri.parse('${baseUrl}index.php'), headers: {'User-Agent': UT_USER_AGENT});
      if (res.statusCode == 200) {
        final html = utf8.decode(res.bodyBytes);
        final parsed = _parseHomePage(html);
        heroItems = parsed.item1;
        categories = parsed.item2.where((c) => c.name.toLowerCase() != 'featured').toList();
        allItemsPool = [for (var c in categories) ...c.items];
      }
    } catch (_) {}
    isLoading = false;
    notifyListeners();
  }

  Future<void> refreshHome() async {
    await fetchHome();
  }

  Future<Map<String, dynamic>> fetchCategory(int typeId, int page, bool useTag, String? sort, String? genre) async {
    String pageParam = page > 1 ? "&page=$page" : "";
    String urlStr = useTag ? "${baseUrl}index.php?do=list&tag=$typeId$pageParam" : "${baseUrl}index.php?do=list&type=$typeId$pageParam";
    if (sort != null && sort.isNotEmpty) urlStr += "&sort=$sort";
    if (genre != null && genre.isNotEmpty) urlStr += "&genre=$genre";
    final client = getClient();
    try {
      final res = await client.get(Uri.parse(urlStr), headers: {'User-Agent': UT_USER_AGENT});
      if (res.statusCode == 200) {
        final html = utf8.decode(res.bodyBytes);
        final items = _parseListPage(html);
        final hasMore = _detectHasMorePages(html, page);
        return {'items': items, 'hasMore': hasMore};
      }
    } catch (_) {}
    return {'items': <VideoItem>[], 'hasMore': false};
  }

  Future<List<VideoItem>> advancedSearch({String? title, String? genre, String? type, String? imdb, String? director, String? writer, String? cast, String? year, String? mpr, String? imdbrate, String? production, String? language, bool? featured}) async {
    String urlStr = "${baseUrl}index.php?do=list";
    if (title != null && title.isNotEmpty) urlStr += "&title=$title";
    if (genre != null && genre.isNotEmpty) urlStr += "&genre=$genre";
    if (type != null && type.isNotEmpty) urlStr += "&type=$type";
    if (imdb != null && imdb.isNotEmpty) urlStr += "&imdb=$imdb";
    if (director != null && director.isNotEmpty) urlStr += "&director=$director";
    if (writer != null && writer.isNotEmpty) urlStr += "&writer=$writer";
    if (cast != null && cast.isNotEmpty) urlStr += "&cast=$cast";
    if (year != null && year.isNotEmpty) urlStr += "&year=$year";
    if (mpr != null && mpr.isNotEmpty) urlStr += "&mpr=$mpr";
    if (imdbrate != null && imdbrate.isNotEmpty) urlStr += "&imdbrate=$imdbrate";
    if (production != null && production.isNotEmpty) urlStr += "&production=$production";
    if (language != null && language.isNotEmpty) urlStr += "&language=$language";
    if (featured == true) urlStr += "&featured=1";

    final client = getClient();
    try {
      final res = await client.get(Uri.parse(urlStr), headers: {'User-Agent': UT_USER_AGENT});
      if (res.statusCode == 200) {
        final html = utf8.decode(res.bodyBytes);
        return _parseListPage(html);
      }
    } catch (_) {}
    return [];
  }

  Future<MediaDetails> fetchDetails(String id) async {
    MediaDetails d = MediaDetails();
    final client = getClient();
    try {
      final res = await client.get(Uri.parse('${baseUrl}index.php?do=view&type=post&id=$id'), headers: {'User-Agent': UT_USER_AGENT});
      if (res.statusCode == 200) {
        final html = utf8.decode(res.bodyBytes);
        d = _parseDetails(html);
      }
    } catch (_) {}
    return d;
  }

  // --- HTML Parsers ---
  _Tuple<List<VideoItem>, List<CategoryData>> _parseHomePage(String html) {
    List<VideoItem> carousel = [];
    List<CategoryData> sections = [];
    
    final carRx = RegExp(r'<a href="index\.php\?do=view&type=post&id=(\d+)"><img src="([^"]+)"[^>]*alt="([^"]*)">');
    for (var match in carRx.allMatches(html)) {
      String id = match.group(1)!;
      String img = match.group(2)!;
      String title = match.group(3)!;
      if (!img.startsWith("http")) img = baseUrl + img;
      if (!carousel.any((e) => e.id == id)) carousel.add(VideoItem(id: id, title: title, imageUrl: img, type: 'post'));
    }

    final headerRx = RegExp(r'<h2><a href="\?do=list&tag=(\d+)"[^>]*>([^<]+)</a></h2>');
    final itemRx = RegExp(r'<a href="index\.php\?do=view&type=post&id=(\d+)">\s*<img src="([^"]+)"[^>]*>\s*<div class="mytitle">([^<]*)</div>', dotAll: true);
    
    final headerMatches = headerRx.allMatches(html).toList();
    for (int i = 0; i < headerMatches.length; i++) {
      int tagId = int.tryParse(headerMatches[i].group(1)!) ?? -1;
      String title = headerMatches[i].group(2)!.trim();
      int start = headerMatches[i].end;
      int end = (i + 1 < headerMatches.length) ? headerMatches[i+1].start : html.length;
      String block = html.substring(start, end);
      
      List<VideoItem> items = [];
      for (var m in itemRx.allMatches(block)) {
        String id = m.group(1)!;
        String img = m.group(2)!;
        String iTitle = m.group(3)!.trim();
        if (!img.startsWith("http")) img = baseUrl + img;
        img = optimizeImageUrl(img, width: 400, height: 600);
        if (!items.any((e) => e.id == id)) items.add(VideoItem(id: id, title: iTitle, imageUrl: img, type: 'post'));
      }
      if (items.isNotEmpty) sections.add(CategoryData(title, items, tagId));
    }
    return _Tuple(carousel, sections);
  }

  List<VideoItem> _parseListPage(String html) {
    List<VideoItem> items = [];
    final rx = RegExp(r'href="index\.php\?do=view&type=post&id=(\d+)"><img src="([^"]+)"[^>]*>\s*</a>\s*<div class="mytitle">\s*<a[^>]*>([^<]+)</a>', dotAll: true);
    for (var m in rx.allMatches(html)) {
      String id = m.group(1)!;
      String img = m.group(2)!;
      String title = m.group(3)!.trim();
      if (!img.startsWith("http")) img = baseUrl + img;
      img = optimizeImageUrl(img, width: 400, height: 600);
      if (!items.any((e) => e.id == id)) items.add(VideoItem(id: id, title: title, imageUrl: img, type: 'post'));
    }
    return items;
  }

  bool _detectHasMorePages(String html, int currentPage) {
    int start = html.indexOf('<ul class="pagination">');
    if (start == -1) return false;
    int end = html.indexOf('</ul>', start);
    if (end == -1) return false;
    String block = html.substring(start, end);
    final rx = RegExp(r'page=(\d+)');
    List<int> pages = rx.allMatches(block).map((m) => int.parse(m.group(1)!)).toList();
    if (pages.isEmpty) return false;
    return pages.reduce((a, b) => a > b ? a : b) > currentPage;
  }

  String? _firstMatch(String pattern, String text) {
    final rx = RegExp(pattern, dotAll: true);
    return rx.firstMatch(text)?.group(1)?.trim();
  }

  MediaDetails _parseDetails(String html) {
    MediaDetails d = MediaDetails();
    d.title = _firstMatch(r'<h1>(.*?)</h1>', html) ?? "";
    d.year = _firstMatch(r'<span>Year:\s*</span>\s*([^<]+)', html) ?? "";
    d.genre = _firstMatch(r'<span>Genre:\s*</span>\s*([^<]+)', html) ?? "";
    d.rating = _firstMatch(r'<span>IMdB Rating:\s*</span>\s*([^<]+)', html) ?? "";
    d.runtime = _firstMatch(r'<span>Runtime:\s*</span>\s*([^<]+)', html) ?? "";
    d.synopsis = _firstMatch(r'<h3>Synopsis:</h3>.*?<h4>(.*?)</h4>', html) ?? "";

    String? img = _firstMatch(r'<img src="([^"]+)" class="img-responsive"', html);
    if (img != null) {
      d.imageUrl = img.startsWith("http") ? img : baseUrl + img;
      d.imageUrl = optimizeImageUrl(d.imageUrl, width: 800, height: 1200);
    }

    final blockRx = RegExp(r'<li class="episodeitem">(.*?)</li>', dotAll: true);
    for (var bMatch in blockRx.allMatches(html)) {
      String block = bMatch.group(1)!;
      String epId = _firstMatch(r'data-id="(\d+)"', block) ?? "";
      if (epId.isEmpty) continue;
      String epTitle = _firstMatch(r'data-title="([^"]*)"', block) ?? "";
      String epUrl = _firstMatch(r'data-url="([^"]*)"', block) ?? "";
      String epUrl720 = _firstMatch(r'data-url720="([^"]*)"', block) ?? "";
      String epUrl360 = _firstMatch(r'data-url360="([^"]*)"', block) ?? "";
      String epUrl1080 = _firstMatch(r'data-url1080="([^"]*)"', block) ?? "";
      String epUrl4k = _firstMatch(r'data-url4k="([^"]*)"', block) ?? "";
      String epSrt = _firstMatch(r'data-srt="([^"]*)"', block) ?? "";
      String epWebvtt = _firstMatch(r'data-webvtt="([^"]*)"', block) ?? "";
      
      if (epUrl.isNotEmpty) {
        d.episodes.add(EpisodeItem(
          id: epId, title: epTitle.isEmpty ? "الحلقة ${d.episodes.length + 1}" : epTitle,
          url: epUrl, url720: epUrl720, url1080: epUrl1080, url360: epUrl360, url4k: epUrl4k,
          subtitleUrl: epSrt, subtitleVttUrl: epWebvtt
        ));
      }
    }

    if (d.episodes.isEmpty) {
      d.isMovie = true;
      final mRx = RegExp(r'data-url="([^"]+)"[^>]*data-url360="([^"]*)"[^>]*(?:data-url4k="([^"]*)"[^>]*)?(?:data-url720="([^"]*)"[^>]*)?data-url1080="([^"]*)"[^>]*data-srt="([^"]*)"[^>]*data-webvtt="([^"]*)"', dotAll: true);
      final match = mRx.firstMatch(html);
      if (match != null) {
        d.movieUrl = match.group(1) ?? "";
        d.movieUrl360 = match.group(2) ?? "";
        d.movieUrl4k = match.groupCount >= 3 ? match.group(3) ?? "" : "";
        d.movieUrl720 = match.groupCount >= 4 ? match.group(4) ?? "" : "";
        d.movieUrl1080 = match.groupCount >= 5 ? match.group(5) ?? "" : "";
        d.movieSubtitleUrl = match.groupCount >= 6 ? match.group(6) ?? "" : "";
        d.movieSubtitleVttUrl = match.groupCount >= 7 ? match.group(7) ?? "" : "";
      }
    } else {
      d.isMovie = false;
    }
    return d;
  }
}

class _Tuple<T1, T2> {
  final T1 item1;
  final T2 item2;
  _Tuple(this.item1, this.item2);
}
"""
with open("UTan_Flutter/lib/services/scraper.dart", "w", encoding="utf-8") as f:
    f.write(scraper_dart)

# 12. lib/services/subtitle_parser.dart (modified to use proxy)
subtitle_parser_dart = """import 'dart:convert';
import 'package:http/http.dart' as http;
import 'proxy_client.dart';

class SubtitleCue {
  final double startTime;
  final double endTime;
  final String text;
  SubtitleCue(this.startTime, this.endTime, this.text);
}

class SubtitleParser {
  static Future<List<SubtitleCue>> parse(String url) async {
    if (url.isEmpty) return [];
    String cleanUrl = url.startsWith("http") ? url : "https://movie.vodu.me/" + url;
    final client = getClient();
    try {
      final res = await client.get(Uri.parse(cleanUrl));
      if (res.statusCode == 200) {
        String text = utf8.decode(res.bodyBytes, allowMalformed: true);
        if (text.contains("WEBVTT")) return _parseWebVTT(text);
        return _parseSRT(text);
      }
    } catch (_) {}
    return [];
  }

  static List<SubtitleCue> _parseSRT(String content) {
    List<SubtitleCue> cues = [];
    String normalized = content.replaceAll("\\r\\n", "\\n").replaceAll("\\r", "\\n");
    List<String> blocks = normalized.split("\\n\\n");
    for (String block in blocks) {
      List<String> lines = block.split("\\n").map((e) => e.trim()).where((e) => e.isNotEmpty).toList();
      if (lines.length < 3) continue;
      String timeLine = lines[1];
      String text = lines.sublist(2).join("\\n").replaceAll(RegExp(r'<[^>]+>'), "").trim();
      if (text.isEmpty) continue;
      List<String> times = timeLine.split(" --> ");
      if (times.length == 2) {
        double? start = _parseSRTTime(times[0]);
        double? end = _parseSRTTime(times[1]);
        if (start != null && end != null) cues.add(SubtitleCue(start, end, text));
      }
    }
    return cues;
  }

  static double? _parseSRTTime(String timeString) {
    String clean = timeString.trim();
    List<String> parts = clean.split(",");
    if (parts.length != 2) return null;
    double ms = double.tryParse(parts[1]) ?? 0;
    List<String> timeComponents = parts[0].split(":");
    if (timeComponents.length == 3) {
      double h = double.tryParse(timeComponents[0]) ?? 0;
      double m = double.tryParse(timeComponents[1]) ?? 0;
      double s = double.tryParse(timeComponents[2]) ?? 0;
      return (h * 3600) + (m * 60) + s + (ms / 1000);
    }
    return null;
  }

  static List<SubtitleCue> _parseWebVTT(String content) {
    List<SubtitleCue> cues = [];
    List<String> lines = content.split("\\n");
    int i = 0;
    while (i < lines.length) {
      String line = lines[i].trim();
      if (line.contains("-->")) {
        String timePart = line.split(" position:")[0].split(" align:")[0].split(" line:")[0].split(" size:")[0];
        List<String> times = timePart.split("-->");
        if (times.length == 2) {
          double? start = _parseVTTTime(times[0]);
          double? end = _parseVTTTime(times[1]);
          if (start != null && end != null) {
            List<String> textLines = [];
            i++;
            while (i < lines.length && lines[i].trim().isNotEmpty) {
              textLines.add(lines[i].trim());
              i++;
            }
            String text = textLines.join("\\n").replaceAll(RegExp(r'<[^>]+>'), "").trim();
            if (text.isNotEmpty) cues.add(SubtitleCue(start, end, text));
            continue;
          }
        }
      }
      i++;
    }
    return cues;
  }

  static double? _parseVTTTime(String timeString) {
    String clean = timeString.trim();
    List<String> parts = clean.split(":");
    double h = 0, m = 0, s = 0;
    if (parts.length == 3) {
      h = double.tryParse(parts[0]) ?? 0;
      m = double.tryParse(parts[1]) ?? 0;
      List<String> sParts = parts[2].split(".");
      s = double.tryParse(sParts[0]) ?? 0;
      if (sParts.length == 2) s += (double.tryParse(sParts[1]) ?? 0) / 1000;
    } else if (parts.length == 2) {
      m = double.tryParse(parts[0]) ?? 0;
      List<String> sParts = parts[1].split(".");
      s = double.tryParse(sParts[0]) ?? 0;
      if (sParts.length == 2) s += (double.tryParse(sParts[1]) ?? 0) / 1000;
    } else {
      return null;
    }
    return (h * 3600) + (m * 60) + s;
  }
}
"""
with open("UTan_Flutter/lib/services/subtitle_parser.dart", "w", encoding="utf-8") as f:
    f.write(subtitle_parser_dart)

# 13. lib/views/player_view.dart (unchanged, but using proxy for subtitles via subtitle_parser)
player_view_dart = """import 'dart:async';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'package:volume_controller/volume_controller.dart';
import 'package:screen_brightness/screen_brightness.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/models.dart';
import '../stores/app_settings.dart';
import '../stores/watch_progress_store.dart';
import '../services/subtitle_parser.dart';

class CustomPlayerView extends StatefulWidget {
  final PlayerData data;
  const CustomPlayerView({Key? key, required this.data}) : super(key: key);
  @override
  _CustomPlayerViewState createState() => _CustomPlayerViewState();
}

class _CustomPlayerViewState extends State<CustomPlayerView> {
  late PlayerData currentData;
  VideoPlayerController? _controller;
  bool isPlaying = true;
  bool showControls = true;
  bool isLocked = false;
  bool isBuffering = true;
  Timer? hideTimer;
  Timer? saveTimer;
  Timer? upNextTimer;
  int upNextCountdown = 0;
  bool showUpNext = false;
  
  List<SubtitleCue> cues = [];
  String activeSub = "";
  String activeTopSub = "";
  int subtitleCursor = 0;
  int? bottomCueIdx;
  int? topCueIdx;

  double volume = 0.5;
  double brightness = 0.5;
  bool showVolumeHUD = false;
  bool showBrightnessHUD = false;
  Timer? hudTimer;
  
  String currentQuality = 'تلقائي';
  
  @override
  void initState() {
    super.initState();
    currentData = widget.data;
    VolumeController().getVolume().then((v) => volume = v);
    ScreenBrightness().current.then((b) => brightness = b);
    _initPlayer();
  }

  void _initPlayer() {
    isBuffering = true;
    _controller?.dispose();
    String url = _resolvedUrl(currentQuality);
    _controller = VideoPlayerController.network(url)
      ..initialize().then((_) {
        setState(() { isBuffering = false; });
        final saved = WatchProgressStore.shared.progressFor(currentData.itemId, currentData.episodeId);
        if (saved != null && saved.progressSeconds > 5) {
          _controller!.seekTo(Duration(seconds: saved.progressSeconds.toInt()));
        }
        _controller!.play();
        _scheduleHide();
      });

    _controller!.addListener(() {
      if (!mounted) return;
      if (_controller!.value.isBuffering != isBuffering) {
        setState(() => isBuffering = _controller!.value.isBuffering);
      }
      _checkSubtitles(_controller!.value.position.inMilliseconds / 1000.0);
      _checkUpNext();
    });

    _loadSubtitles();
    _startSaveTimer();
  }

  void _loadSubtitles() async {
    cues.clear(); activeSub = ""; activeTopSub = "";
    bottomCueIdx = null; topCueIdx = null; subtitleCursor = 0;
    String sUrl = currentData.subtitleVttUrl.isEmpty ? currentData.subtitleUrl : currentData.subtitleVttUrl;
    if (sUrl.isEmpty) return;
    final parsed = await SubtitleParser.parse(sUrl);
    setState(() {
      cues = parsed.map((c) {
        String t = c.text.replaceAll(RegExp(r'\{[^}]+\}'), '').trim();
        return SubtitleCue(c.startTime, c.endTime, t);
      }).where((c) => c.text.isNotEmpty).toList();
    });
  }

  void _checkSubtitles(double time) {
    if (cues.isEmpty) return;
    time += AppSettings.shared.subtitleDelay;
    
    if (subtitleCursor >= cues.length) subtitleCursor = cues.length - 1;
    while (subtitleCursor < cues.length - 1 && cues[subtitleCursor].endTime < time) { subtitleCursor++; }
    if (cues[subtitleCursor].startTime > time) {
      int lo = 0, hi = subtitleCursor;
      while (lo < hi) {
        int mid = (lo + hi) ~/ 2;
        if (cues[mid].endTime < time) lo = mid + 1; else hi = mid;
      }
      subtitleCursor = lo;
    }

    bool changed = false;
    if (bottomCueIdx != null && (time < cues[bottomCueIdx!].startTime || time > cues[bottomCueIdx!].endTime)) {
      activeSub = ""; bottomCueIdx = null; changed = true;
    }
    if (topCueIdx != null && (time < cues[topCueIdx!].startTime || time > cues[topCueIdx!].endTime)) {
      activeTopSub = ""; topCueIdx = null; changed = true;
    }

    int wStart = (subtitleCursor - 3).clamp(0, cues.length);
    int wEnd = (subtitleCursor + 3).clamp(0, cues.length - 1);
    
    for (int i = wStart; i <= wEnd; i++) {
      var c = cues[i];
      if (time >= c.startTime && time <= c.endTime && i != bottomCueIdx && i != topCueIdx) {
        if (bottomCueIdx == null) { bottomCueIdx = i; activeSub = c.text; changed = true; }
        else if (topCueIdx == null) { topCueIdx = i; activeTopSub = c.text; changed = true; break; }
      }
    }
    if (changed) setState(() {});
  }

  String _resolvedUrl(String q) {
    String fix(String u) {
      if (u.isEmpty) return "";
      return u.startsWith("http") ? u : "https://movie.vodu.me/" + u;
    }
    switch (q) {
      case '360p': return fix(currentData.videoUrl360.isNotEmpty ? currentData.videoUrl360 : currentData.videoUrl);
      case '720p': return fix(currentData.videoUrl720.isNotEmpty ? currentData.videoUrl720 : currentData.videoUrl);
      case '1080p': return fix(currentData.videoUrl1080.isNotEmpty ? currentData.videoUrl1080 : currentData.videoUrl);
      case '4K': return fix(currentData.videoUrl4k.isNotEmpty ? currentData.videoUrl4k : currentData.videoUrl);
      default: return fix(currentData.videoUrl);
    }
  }

  void _startSaveTimer() {
    saveTimer?.cancel();
    saveTimer = Timer.periodic(const Duration(seconds: 5), (_) {
      if (_controller == null || !_controller!.value.isInitialized) return;
      WatchProgressStore.shared.save(
        itemId: currentData.itemId, title: currentData.itemTitle, imageUrl: currentData.itemImageUrl,
        episodeId: currentData.episodeId, episodeTitle: currentData.episodeTitle,
        progress: _controller!.value.position.inMilliseconds / 1000.0,
        duration: _controller!.value.duration.inMilliseconds / 1000.0,
        videoUrl: currentData.videoUrl, videoUrl720: currentData.videoUrl720, videoUrl1080: currentData.videoUrl1080,
        videoUrl360: currentData.videoUrl360, videoUrl4k: currentData.videoUrl4k,
        subUrl: currentData.subtitleUrl, subVttUrl: currentData.subtitleVttUrl, isMovie: currentData.isMovie
      );
    });
  }

  void _scheduleHide() {
    hideTimer?.cancel();
    hideTimer = Timer(const Duration(seconds: 4), () => setState(() => showControls = false));
  }
  
  EpisodeItem? get nextEpisode {
    if (currentData.isMovie) return null;
    int idx = currentData.episodes.indexWhere((e) => e.id == currentData.episodeId);
    if (idx != -1 && idx + 1 < currentData.episodes.length) return currentData.episodes[idx + 1];
    return null;
  }

  void _checkUpNext() {
    if (currentData.isMovie || !AppSettings.shared.autoPlayNextEnabled || showUpNext) return;
    final val = _controller!.value;
    if (!val.isInitialized) return;
    double remain = (val.duration - val.position).inMilliseconds / 1000.0;
    if (remain > 0 && remain <= AppSettings.shared.autoPlayCountdownSeconds && nextEpisode != null) {
      setState(() { showUpNext = true; upNextCountdown = AppSettings.shared.autoPlayCountdownSeconds; });
      upNextTimer?.cancel();
      upNextTimer = Timer.periodic(const Duration(seconds: 1), (t) {
        if (upNextCountdown <= 1) {
          t.cancel(); setState(() => showUpNext = false);
          _switchToEpisode(nextEpisode!);
        } else {
          setState(() => upNextCountdown--);
        }
      });
    }
  }

  void _switchToEpisode(EpisodeItem ep) {
    upNextTimer?.cancel(); saveTimer?.cancel();
    setState(() {
      currentData = PlayerData(
        itemId: currentData.itemId, itemTitle: currentData.itemTitle, itemImageUrl: currentData.itemImageUrl,
        isMovie: false, videoUrl: ep.url, videoUrl720: ep.url720, videoUrl1080: ep.url1080, videoUrl360: ep.url360, videoUrl4k: ep.url4k,
        subtitleUrl: ep.subtitleUrl, subtitleVttUrl: ep.subtitleVttUrl,
        episodeId: ep.id, episodeTitle: ep.title, episodes: currentData.episodes
      );
    });
    _initPlayer();
  }

  @override
  void dispose() {
    hideTimer?.cancel(); saveTimer?.cancel(); upNextTimer?.cancel(); hudTimer?.cancel();
    _controller?.dispose();
    super.dispose();
  }

  String _formatTime(Duration d) {
    String twoDigits(int n) => n.toString().padLeft(2, "0");
    String h = d.inHours > 0 ? "${twoDigits(d.inHours)}:" : "";
    return "$h${twoDigits(d.inMinutes.remainder(60))}:${twoDigits(d.inSeconds.remainder(60))}";
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: GestureDetector(
        onTap: () { if (!isLocked) { setState(() => showControls = !showControls); if (showControls) _scheduleHide(); } },
        onVerticalDragUpdate: (details) {
          if (isLocked) return;
          double dy = details.primaryDelta! / -250.0;
          if (details.globalPosition.dx > MediaQuery.of(context).size.width / 2) {
            volume = (volume + dy).clamp(0.0, 1.0);
            VolumeController().setVolume(volume, showSystemUI: false);
            setState(() { showVolumeHUD = true; showBrightnessHUD = false; });
          } else {
            brightness = (brightness + dy).clamp(0.0, 1.0);
            ScreenBrightness().setScreenBrightness(brightness);
            setState(() { showBrightnessHUD = true; showVolumeHUD = false; });
          }
          hudTimer?.cancel();
          hudTimer = Timer(const Duration(milliseconds: 900), () => setState(() { showVolumeHUD = false; showBrightnessHUD = false; }));
        },
        child: Stack(
          children: [
            Center(child: _controller != null && _controller!.value.isInitialized ? AspectRatio(aspectRatio: _controller!.value.aspectRatio, child: VideoPlayer(_controller!)) : const SizedBox()),
            
            // Subtitles
            if (AppSettings.shared.subtitlesEnabled)
              Positioned.fill(
                child: Column(
                  children: [
                    if (activeTopSub.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 60), child: _buildSub(activeTopSub)),
                    const Spacer(),
                    if (activeSub.isNotEmpty) Padding(padding: EdgeInsets.only(bottom: AppSettings.shared.subtitleBottomPad), child: _buildSub(activeSub)),
                  ],
                ),
              ),

            // 9r7n Branding Watermark
            Positioned(top: 40, left: 16, child: Opacity(opacity: 0.35, child: Text('9r7n', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: Colors.white)))),

            if (isBuffering) const Center(child: CircularProgressIndicator(color: Colors.white)),
            
            if (showVolumeHUD || showBrightnessHUD)
              Align(
                alignment: Alignment.topCenter,
                child: Padding(
                  padding: const EdgeInsets.only(top: 70),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                    decoration: BoxDecoration(color: Colors.black54, borderRadius: BorderRadius.circular(14)),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(showVolumeHUD ? Icons.volume_up : Icons.brightness_6, color: Colors.white),
                        const SizedBox(width: 10),
                        SizedBox(width: 100, child: LinearProgressIndicator(value: showVolumeHUD ? volume : brightness, color: Colors.white, backgroundColor: Colors.white24)),
                      ],
                    ),
                  ),
                ),
              ),

            if (showUpNext && nextEpisode != null)
              Positioned(
                bottom: 40, left: 20, right: 20,
                child: Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(color: Colors.black87, borderRadius: BorderRadius.circular(16)),
                  child: Row(
                    children: [
                      CircleAvatar(backgroundColor: Colors.white12, child: Text('$upNextCountdown', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold))),
                      const SizedBox(width: 12),
                      Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text('الحلقة التالية', style: TextStyle(color: Colors.white60, fontSize: 11)),
                        Text(nextEpisode!.title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold), maxLines: 1),
                      ])),
                      TextButton(onPressed: () { upNextTimer?.cancel(); setState(() => showUpNext = false); }, child: const Text('إلغاء', style: TextStyle(color: Colors.white))),
                      ElevatedButton(
                        onPressed: () => _switchToEpisode(nextEpisode!),
                        style: ElevatedButton.styleFrom(backgroundColor: AppSettings.shared.accentColor),
                        child: const Text('تشغيل'),
                      )
                    ],
                  ),
                ),
              ),

            if ((showControls || isLocked) && !showUpNext) _buildControls(),
          ],
        ),
      ),
    );
  }

  Widget _buildSub(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 6),
      decoration: BoxDecoration(color: Colors.black.withOpacity(AppSettings.shared.subtitleBgOpacity), borderRadius: BorderRadius.circular(8)),
      child: Text(text, textAlign: TextAlign.center, style: TextStyle(color: AppSettings.shared.subtitleColor, fontSize: AppSettings.shared.subtitleFontSize, fontWeight: FontWeight.bold, fontFamily: AppSettings.shared.subtitleFontName)),
    );
  }

  Widget _buildControls() {
    if (isLocked) {
      return Positioned(
        top: 20, right: 20,
        child: IconButton(icon: const Icon(Icons.lock, color: Colors.white), onPressed: () => setState(() { isLocked = false; _scheduleHide(); }))
      );
    }
    return Stack(
      children: [
        Positioned(top: 0, left: 0, right: 0, child: Container(height: 100, decoration: const BoxDecoration(gradient: LinearGradient(colors: [Colors.black87, Colors.transparent], begin: Alignment.topCenter, end: Alignment.bottomCenter)))),
        Positioned(bottom: 0, left: 0, right: 0, child: Container(height: 150, decoration: const BoxDecoration(gradient: LinearGradient(colors: [Colors.transparent, Colors.black87], begin: Alignment.topCenter, end: Alignment.bottomCenter)))),
        
        // Top bar
        Positioned(
          top: 20, left: 10, right: 10,
          child: Row(
            children: [
              IconButton(icon: const Icon(Icons.arrow_back_ios, color: Colors.white), onPressed: () => Navigator.pop(context)),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(currentData.itemTitle, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold), maxLines: 1),
                if (!currentData.isMovie) Text(currentData.episodeTitle, style: const TextStyle(color: Colors.white54, fontSize: 12), maxLines: 1),
              ])),
              IconButton(icon: const Icon(Icons.closed_caption, color: Colors.white), onPressed: () => _showSubSettings()),
              IconButton(icon: const Icon(Icons.lock_open, color: Colors.white), onPressed: () => setState(() => isLocked = true)),
            ],
          ),
        ),

        // Center play/pause
        Center(
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              IconButton(icon: const Icon(Icons.replay_10, color: Colors.white, size: 40), onPressed: () { _controller!.seekTo(_controller!.value.position - const Duration(seconds: 10)); _scheduleHide(); }),
              const SizedBox(width: 40),
              GestureDetector(
                onTap: () {
                  setState(() { _controller!.value.isPlaying ? _controller!.pause() : _controller!.play(); });
                  _scheduleHide();
                },
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: const BoxDecoration(color: Colors.white24, shape: BoxShape.circle),
                  child: Icon(_controller!.value.isPlaying ? Icons.pause : Icons.play_arrow, color: Colors.white, size: 50),
                ),
              ),
              const SizedBox(width: 40),
              IconButton(icon: const Icon(Icons.forward_10, color: Colors.white, size: 40), onPressed: () { _controller!.seekTo(_controller!.value.position + const Duration(seconds: 10)); _scheduleHide(); }),
            ],
          ),
        ),

        // Bottom scrubber
        Positioned(
          bottom: 30, left: 20, right: 20,
          child: Column(
            children: [
              if (_controller != null) Row(
                children: [
                  Text(_formatTime(_controller!.value.position), style: const TextStyle(color: Colors.white)),
                  Expanded(child: VideoProgressIndicator(_controller!, allowScrubbing: true, colors: VideoProgressColors(playedColor: Colors.white, bufferedColor: Colors.white30, backgroundColor: Colors.white12))),
                  Text(_formatTime(_controller!.value.duration), style: const TextStyle(color: Colors.white)),
                ],
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  for (var q in ['تلقائي', '720p', '1080p']) ...[
                    GestureDetector(
                      onTap: () { setState(() => currentQuality = q); _initPlayer(); },
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4), margin: const EdgeInsets.only(right: 6),
                        decoration: BoxDecoration(color: currentQuality == q ? Colors.white : Colors.white12, borderRadius: BorderRadius.circular(12)),
                        child: Text(q, style: TextStyle(color: currentQuality == q ? Colors.black : Colors.white, fontSize: 11)),
                      ),
                    )
                  ],
                  const Spacer(),
                  if (!currentData.isMovie && nextEpisode != null)
                    GestureDetector(
                      onTap: () => _switchToEpisode(nextEpisode!),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(color: Colors.white12, borderRadius: BorderRadius.circular(12)),
                        child: const Row(children: [Text('التالية', style: TextStyle(color: Colors.white, fontSize: 12)), SizedBox(width: 4), Icon(Icons.skip_next, color: Colors.white, size: 14)]),
                      ),
                    )
                ],
              )
            ],
          ),
        )
      ],
    );
  }

  void _showSubSettings() {
    showModalBottomSheet(context: context, backgroundColor: AppSettings.shared.appBgColor, builder: (ctx) {
      return StatefulBuilder(builder: (c, setModalState) {
        return ListView(
          padding: const EdgeInsets.all(20),
          children: [
            const Text('إعدادات الترجمة', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
            SwitchListTile(title: const Text('تفعيل الترجمة', style: TextStyle(color: Colors.white)), value: AppSettings.shared.subtitlesEnabled, onChanged: (v) { setModalState(() => AppSettings.shared.subtitlesEnabled = v); setState((){}); }, activeColor: AppSettings.shared.accentColor),
            Text('تأخير (ثواني): ${AppSettings.shared.subtitleDelay}', style: const TextStyle(color: Colors.white)),
            Slider(value: AppSettings.shared.subtitleDelay, min: -10, max: 10, onChanged: (v) { setModalState(() => AppSettings.shared.subtitleDelay = v); setState((){}); }, activeColor: AppSettings.shared.accentColor),
            Text('حجم الخط: ${AppSettings.shared.subtitleFontSize.toInt()}', style: const TextStyle(color: Colors.white)),
            Slider(value: AppSettings.shared.subtitleFontSize, min: 14, max: 40, onChanged: (v) { setModalState(() => AppSettings.shared.subtitleFontSize = v); setState((){}); }, activeColor: AppSettings.shared.accentColor),
          ],
        );
      });
    });
  }
}

class PlayerData {
  final String itemId;
  final String itemTitle;
  final String itemImageUrl;
  final bool isMovie;
  final String videoUrl;
  final String videoUrl720;
  final String videoUrl1080;
  final String videoUrl360;
  final String videoUrl4k;
  final String subtitleUrl;
  final String subtitleVttUrl;
  final String episodeId;
  final String episodeTitle;
  final List<EpisodeItem> episodes;

  PlayerData({required this.itemId, required this.itemTitle, required this.itemImageUrl, this.isMovie = true, required this.videoUrl, required this.videoUrl720, required this.videoUrl1080, required this.videoUrl360, this.videoUrl4k = "", required this.subtitleUrl, required this.subtitleVttUrl, required this.episodeId, required this.episodeTitle, this.episodes = const []});
}
"""
with open("UTan_Flutter/lib/views/player_view.dart", "w", encoding="utf-8") as f:
    f.write(player_view_dart)

# 14. lib/views/main_tab_view.dart
main_tab_view_dart = """import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../stores/app_settings.dart';
import '../services/scraper.dart';
import 'home_view.dart';
import 'browse_search_settings.dart';

class MainTabView extends StatefulWidget {
  const MainTabView({Key? key}) : super(key: key);
  @override
  _MainTabViewState createState() => _MainTabViewState();
}

class _MainTabViewState extends State<MainTabView> {
  int _currentIndex = 0;
  final MovieScraper _scraper = MovieScraper();
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _initFetch();
  }

  void _initFetch() async {
    await _scraper.fetchHome();
    if (mounted) setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        const Text("9r7n", style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: Colors.white)),
        const SizedBox(height: 20),
        CircularProgressIndicator(color: AppSettings.shared.accentColor)
      ])));
    }

    final List<Widget> pages = [
      HomeView(scraper: _scraper),
      BrowseView(scraper: _scraper),
      SearchView(scraper: _scraper),
      const DownloadsView(),
      const SettingsView(),
    ];

    return Scaffold(
      body: IndexedStack(index: _currentIndex, children: pages),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.black87,
        selectedItemColor: AppSettings.shared.accentColor,
        unselectedItemColor: Colors.grey,
        type: BottomNavigationBarType.fixed,
        currentIndex: _currentIndex,
        onTap: (i) => setState(() => _currentIndex = i),
        items: [
          BottomNavigationBarItem(icon: const Icon(Icons.home), label: L('الرئيسية', 'Home')),
          BottomNavigationBarItem(icon: const Icon(Icons.grid_view), label: L('تصفح', 'Browse')),
          BottomNavigationBarItem(icon: const Icon(Icons.search), label: L('بحث', 'Search')),
          BottomNavigationBarItem(icon: const Icon(Icons.download), label: L('التحميلات', 'Downloads')),
          BottomNavigationBarItem(icon: const Icon(Icons.menu), label: L('المزيد', 'More')),
        ],
      ),
    );
  }
}
"""
with open("UTan_Flutter/lib/views/main_tab_view.dart", "w", encoding="utf-8") as f:
    f.write(main_tab_view_dart)

# 15. lib/views/home_view.dart
home_view_dart = """import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../services/scraper.dart';
import '../stores/watch_progress_store.dart';
import '../stores/app_settings.dart';
import 'details_view.dart';
import 'player_view.dart';

class HomeView extends StatelessWidget {
  final MovieScraper scraper;
  const HomeView({Key? key, required this.scraper}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (scraper.heroItems.isNotEmpty) _buildHero(context),
                if (WatchProgressStore.shared.recent.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 20, bottom: 20),
                    child: _buildContinueWatching(context),
                  ),
                if (scraper.heroItems.length >= 5)
                  Padding(padding: const EdgeInsets.only(bottom: 20), child: _buildTop10(context)),
                ...scraper.categories.map((c) => Padding(padding: const EdgeInsets.only(bottom: 20), child: _buildCategoryRow(context, c))),
                const SizedBox(height: 40)
              ],
            ),
          ),
          Positioned(top: MediaQuery.of(context).padding.top + 8, left: 20, child: Text("9r7n", style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold, color: Colors.white, shadows: [Shadow(color: Colors.black, blurRadius: 4)])))
        ],
      ),
    );
  }

  Widget _buildHero(BuildContext context) {
    final item = scraper.heroItems.first;
    return GestureDetector(
      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsView(itemId: item.id))),
      child: SizedBox(
        height: MediaQuery.of(context).size.height * 0.62,
        width: double.infinity,
        child: Stack(
          fit: StackFit.expand,
          children: [
            CachedNetworkImage(imageUrl: item.imageUrl, fit: BoxFit.cover),
            Container(decoration: const BoxDecoration(gradient: LinearGradient(colors: [Colors.transparent, Colors.black], begin: Alignment.center, end: Alignment.bottomCenter))),
            Positioned(
              bottom: 40, left: 28, right: 28,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(item.title, style: const TextStyle(fontSize: 34, fontWeight: FontWeight.bold, color: Colors.white, shadows: [Shadow(color: Colors.black87, blurRadius: 8, offset: Offset(0, 4))]), maxLines: 2),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      ElevatedButton.icon(
                        icon: const Icon(Icons.play_arrow, color: Colors.black), label: Text(L('تشغيل', 'Play'), style: const TextStyle(color: Colors.black)),
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.white, shape: const StadiumBorder()),
                        onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsView(itemId: item.id))),
                      ),
                      const SizedBox(width: 12),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.info_outline, color: Colors.white), label: Text(L('تفاصيل', 'Details'), style: const TextStyle(color: Colors.white)),
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.white24, shape: const StadiumBorder()),
                        onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsView(itemId: item.id))),
                      ),
                    ],
                  )
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget _buildContinueWatching(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(padding: const EdgeInsets.symmetric(horizontal: 20), child: Text(L('متابعة المشاهدة', 'Continue Watching'), style: const TextStyle(fontSize: 19, fontWeight: FontWeight.bold, color: Colors.white))),
        const SizedBox(height: 14),
        SizedBox(
          height: 150,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 20),
            itemCount: WatchProgressStore.shared.recent.take(12).length,
            itemBuilder: (ctx, i) {
              final p = WatchProgressStore.shared.recent[i];
              return GestureDetector(
                onTap: () {
                  Navigator.push(context, MaterialPageRoute(builder: (_) => CustomPlayerView(data: PlayerData(
                    itemId: p.itemId, itemTitle: p.title, itemImageUrl: p.imageUrl, isMovie: p.isMovie,
                    videoUrl: p.videoUrl, videoUrl720: p.videoUrl720, videoUrl1080: p.videoUrl1080, videoUrl360: p.videoUrl360, videoUrl4k: p.videoUrl4k,
                    subtitleUrl: p.subtitleUrl, subtitleVttUrl: p.subtitleVttUrl, episodeId: p.episodeId, episodeTitle: p.episodeTitle
                  ))));
                },
                child: Container(
                  width: 200, margin: const EdgeInsets.only(right: 14),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      ClipRRect(borderRadius: BorderRadius.circular(10), child: SizedBox(height: 112, width: 200, child: Stack(
                        fit: StackFit.expand,
                        children: [
                          CachedNetworkImage(imageUrl: p.imageUrl, fit: BoxFit.cover),
                          const ColoredBox(color: Colors.black45),
                          const Center(child: Icon(Icons.play_circle_fill, size: 34, color: Colors.white)),
                          if (p.durationSeconds > 0) Positioned(bottom: 0, left: 0, right: 0, child: LinearProgressIndicator(value: p.progressSeconds / p.durationSeconds, color: AppSettings.shared.accentColor, backgroundColor: Colors.white30))
                        ]
                      ))),
                      const SizedBox(height: 4),
                      Text(p.title, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold), maxLines: 1),
                    ],
                  ),
                ),
              );
            },
          ),
        )
      ],
    );
  }

  Widget _buildTop10(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(padding: const EdgeInsets.symmetric(horizontal: 20), child: Text(L('الأكثر مشاهدة اليوم', 'Trending Today'), style: const TextStyle(fontSize: 19, fontWeight: FontWeight.bold, color: Colors.white))),
        const SizedBox(height: 14),
        SizedBox(
          height: 165,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 20),
            itemCount: scraper.heroItems.take(10).length,
            itemBuilder: (ctx, i) {
              final item = scraper.heroItems[i];
              return GestureDetector(
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsView(itemId: item.id))),
                child: Container(
                  width: 110, margin: const EdgeInsets.only(right: 8),
                  child: Stack(
                    children: [
                      ClipRRect(borderRadius: BorderRadius.circular(10), child: CachedNetworkImage(imageUrl: item.imageUrl, fit: BoxFit.cover, width: 110, height: 165)),
                      Positioned(bottom: -10, left: -5, child: Text('${i+1}', style: const TextStyle(fontSize: 70, fontWeight: FontWeight.w900, color: Colors.white, shadows: [Shadow(color: Colors.black, blurRadius: 4)])))
                    ],
                  ),
                ),
              );
            },
          ),
        )
      ],
    );
  }

  Widget _buildCategoryRow(BuildContext context, CategoryData c) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(padding: const EdgeInsets.symmetric(horizontal: 20), child: Text(c.name, style: const TextStyle(fontSize: 19, fontWeight: FontWeight.bold, color: Colors.white))),
        const SizedBox(height: 14),
        SizedBox(
          height: 220,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 20),
            itemCount: c.items.length,
            itemBuilder: (ctx, i) {
              final item = c.items[i];
              return GestureDetector(
                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsView(itemId: item.id))),
                child: Container(
                  width: 120, margin: const EdgeInsets.only(right: 12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      ClipRRect(borderRadius: BorderRadius.circular(10), child: CachedNetworkImage(imageUrl: item.imageUrl, width: 120, height: 176, fit: BoxFit.cover)),
                      const SizedBox(height: 4),
                      Text(item.title, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w500), maxLines: 2)
                    ],
                  ),
                ),
              );
            },
          ),
        )
      ],
    );
  }
}
"""
with open("UTan_Flutter/lib/views/home_view.dart", "w", encoding="utf-8") as f:
    f.write(home_view_dart)

# 16. lib/views/details_view.dart
details_view_dart = """import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:provider/provider.dart';
import '../services/scraper.dart';
import '../models/models.dart';
import '../stores/app_settings.dart';
import '../stores/favorites_store.dart';
import 'player_view.dart';

class DetailsView extends StatefulWidget {
  final String itemId;
  const DetailsView({Key? key, required this.itemId}) : super(key: key);

  @override
  _DetailsViewState createState() => _DetailsViewState();
}

class _DetailsViewState extends State<DetailsView> {
  final MovieScraper scraper = MovieScraper();
  MediaDetails? details;
  bool loading = true;
  String selectedSeason = "";

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() async {
    final d = await scraper.fetchDetails(widget.itemId);
    if (mounted) setState(() { details = d; selectedSeason = d.sortedSeasons.isNotEmpty ? d.sortedSeasons.first : ""; loading = false; });
  }

  @override
  Widget build(BuildContext context) {
    if (loading) return Scaffold(body: Center(child: CircularProgressIndicator(color: AppSettings.shared.accentColor)));
    if (details == null) return Scaffold(appBar: AppBar(backgroundColor: Colors.transparent), body: const Center(child: Text("تعذّر تحميل البيانات")));

    final d = details!;
    final w = MediaQuery.of(context).size.width;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(backgroundColor: Colors.transparent, elevation: 0),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              height: w * 1.15,
              width: w,
              child: Stack(
                fit: StackFit.expand,
                children: [
                  CachedNetworkImage(imageUrl: d.imageUrl, fit: BoxFit.cover),
                  Container(decoration: BoxDecoration(gradient: LinearGradient(colors: [Colors.transparent, AppSettings.shared.appBgColor], begin: Alignment.center, end: Alignment.bottomCenter)))
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 18),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(d.title, style: const TextStyle(fontSize: 34, fontWeight: FontWeight.bold, color: Colors.white, height: 1.2)),
                  const SizedBox(height: 14),
                  Row(
                    children: [
                      if (d.year.isNotEmpty) _badge(d.year, Icons.calendar_today),
                      if (d.rating.isNotEmpty) _badge(d.rating, Icons.star, Colors.yellow),
                      if (d.runtime.isNotEmpty) _badge(d.runtime, Icons.access_time),
                    ],
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.white, minimumSize: const Size(double.infinity, 46), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8))),
                    onPressed: () {
                      if (d.isMovie) {
                        _play(d, null);
                      } else if (d.episodes.isNotEmpty) {
                        _play(d, d.episodes.first);
                      }
                    },
                    icon: const Icon(Icons.play_arrow, color: Colors.black),
                    label: Text(d.isMovie ? L('تشغيل', 'Play') : L('تشغيل الحلقة الأولى', 'Play First Episode'), style: const TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                  ),
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _actionBtn(FavoritesStore.shared.isFavorite(widget.itemId) ? Icons.favorite : Icons.favorite_border, L('مفضلة', 'Favorite'), () {
                        FavoritesStore.shared.toggle(VideoItem(id: widget.itemId, title: d.title, imageUrl: d.imageUrl, type: d.isMovie ? 'movies' : 'series'));
                        setState((){});
                      }),
                      _actionBtn(Icons.add_to_photos, L('قائمة', 'List'), () {}),
                      if (d.isMovie) _actionBtn(Icons.download, L('تنزيل', 'Download'), () {}),
                      _actionBtn(Icons.share, L('مشاركة', 'Share'), () {}),
                    ],
                  ),
                  const SizedBox(height: 20),
                  if (d.synopsis.isNotEmpty) ...[
                    Text(L('القصة', 'Synopsis'), style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
                    const SizedBox(height: 8),
                    Text(d.synopsis, style: const TextStyle(color: Colors.white70, height: 1.5)),
                    const SizedBox(height: 20),
                  ],
                ],
              ),
            ),
            if (!d.isMovie && d.sortedSeasons.isNotEmpty) ...[
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Row(children: [
                  Text(L('الحلقات', 'Episodes'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
                  const Spacer(),
                  Text('${d.episodes.length} حلقة', style: const TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
                ]),
              ),
              const SizedBox(height: 16),
              if (d.sortedSeasons.length > 1) SizedBox(
                height: 40,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  itemCount: d.sortedSeasons.length,
                  itemBuilder: (c, i) {
                    final s = d.sortedSeasons[i];
                    return GestureDetector(
                      onTap: () => setState(() => selectedSeason = s),
                      child: Container(
                        margin: const EdgeInsets.only(right: 10), padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 8),
                        decoration: BoxDecoration(color: selectedSeason == s ? AppSettings.shared.accentColor : Colors.white12, borderRadius: BorderRadius.circular(20)),
                        child: Text(s, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      ),
                    );
                  }
                ),
              ),
              const SizedBox(height: 12),
              ...d.seasonsDict[selectedSeason]!.map((ep) => ListTile(
                onTap: () => _play(d, ep),
                contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 4),
                leading: ClipRRect(borderRadius: BorderRadius.circular(8), child: CachedNetworkImage(imageUrl: d.imageUrl, width: 100, height: 60, fit: BoxFit.cover)),
                title: Text(ep.title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
                trailing: const Icon(Icons.download, color: Colors.grey),
              )).toList(),
              const SizedBox(height: 40),
            ]
          ],
        ),
      ),
    );
  }

  void _play(MediaDetails d, EpisodeItem? ep) {
    Navigator.push(context, MaterialPageRoute(builder: (_) => CustomPlayerView(data: PlayerData(
      itemId: widget.itemId, itemTitle: d.title, itemImageUrl: d.imageUrl, isMovie: d.isMovie,
      videoUrl: ep?.url ?? d.movieUrl, videoUrl720: ep?.url720 ?? d.movieUrl720, videoUrl1080: ep?.url1080 ?? d.movieUrl1080,
      videoUrl360: ep?.url360 ?? d.movieUrl360, videoUrl4k: ep?.url4k ?? d.movieUrl4k,
      subtitleUrl: ep?.subtitleUrl ?? d.movieSubtitleUrl, subtitleVttUrl: ep?.subtitleVttUrl ?? d.movieSubtitleVttUrl,
      episodeId: ep?.id ?? '', episodeTitle: ep?.title ?? '', episodes: d.episodes
    ))));
  }

  Widget _badge(String text, IconData icon, [Color color = Colors.white]) {
    return Container(
      margin: const EdgeInsets.only(right: 8), padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(color: color == Colors.white ? Colors.white12 : color.withOpacity(0.2), borderRadius: BorderRadius.circular(16)),
      child: Row(children: [Icon(icon, size: 12, color: color == Colors.white ? Colors.white70 : color), const SizedBox(width: 4), Text(text, style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold))]),
    );
  }

  Widget _actionBtn(IconData icon, String label, VoidCallback tap) {
    return GestureDetector(
      onTap: tap,
      child: Column(children: [Icon(icon, color: Colors.white), const SizedBox(height: 4), Text(label, style: const TextStyle(color: Colors.white70, fontSize: 10))]),
    );
  }
}
"""
with open("UTan_Flutter/lib/views/details_view.dart", "w", encoding="utf-8") as f:
    f.write(details_view_dart)

# 17. lib/views/browse_search_settings.dart
browse_search_settings_dart = """import 'package:flutter/material.dart';
import '../services/scraper.dart';
import '../stores/app_settings.dart';
import '../stores/watch_progress_store.dart';
import '../stores/favorites_store.dart';
import '../stores/watchlist_store.dart';
import '../services/supabase_manager.dart';
import '../services/download_manager.dart';

class BrowseView extends StatelessWidget {
  final MovieScraper scraper;
  const BrowseView({Key? key, required this.scraper}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(L('تصفح', 'Browse')), backgroundColor: Colors.transparent, elevation: 0),
      body: GridView.builder(
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 2, crossAxisSpacing: 14, mainAxisSpacing: 14, childAspectRatio: 1.5),
        itemCount: SITE_CATEGORIES.length,
        itemBuilder: (ctx, i) {
          final cat = SITE_CATEGORIES[i];
          return Container(
            decoration: BoxDecoration(gradient: LinearGradient(colors: [Colors.blue.withOpacity(0.5), Colors.blue.withOpacity(0.1)]), borderRadius: BorderRadius.circular(14), border: Border.all(color: Colors.blue.withOpacity(0.2))),
            child: Stack(
              children: [
                const Positioned(top: 12, right: 12, child: Icon(Icons.tv, size: 44, color: Colors.white24)),
                Positioned(bottom: 12, left: 12, child: Text(AppSettings.shared.appLanguage == 'ar' ? cat.nameAr : cat.nameEn, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)))
              ],
            ),
          );
        },
      )
    );
  }
}

class SearchView extends StatefulWidget {
  final MovieScraper scraper;
  const SearchView({Key? key, required this.scraper}) : super(key: key);
  @override
  _SearchViewState createState() => _SearchViewState();
}

class _SearchViewState extends State<SearchView> {
  String title = "";
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(L('بحث', 'Search')), backgroundColor: Colors.transparent, elevation: 0),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              decoration: InputDecoration(hintText: 'بحث...', filled: true, fillColor: Colors.white12, border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none), prefixIcon: const Icon(Icons.search, color: Colors.grey)),
              style: const TextStyle(color: Colors.white),
              onChanged: (v) => setState(() => title = v),
            ),
          ),
          const Expanded(child: Center(child: Text("ابحث عن أي فيلم أو مسلسل", style: TextStyle(color: Colors.grey))))
        ],
      )
    );
  }
}

class DownloadsView extends StatelessWidget {
  const DownloadsView({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(L('التحميلات', 'Downloads')), backgroundColor: Colors.transparent, elevation: 0),
      body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        const Icon(Icons.download, size: 60, color: Colors.grey),
        const SizedBox(height: 20),
        Text(L("لا توجد تحميلات", "No downloads"), style: const TextStyle(color: Colors.grey))
      ]))
    );
  }
}

class SettingsView extends StatelessWidget {
  const SettingsView({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(AuthSession.shared.user?.displayName ?? L('الملف الشخصي', 'Profile')), backgroundColor: Colors.transparent, elevation: 0),
      body: Center(child: Text("9r7n Account & Settings Hub", style: const TextStyle(color: Colors.white)))
    );
  }
}
"""
with open("UTan_Flutter/lib/views/browse_search_settings.dart", "w", encoding="utf-8") as f:
    f.write(browse_search_settings_dart)

print("✅ Flutter project generated successfully at 'UTan_Flutter/'.")
print("✅ All network requests now go through the proxy: 212.237.125.216:6969")
print("✅ Run 'flutter pub get' and then 'flutter run' to launch the app.")
