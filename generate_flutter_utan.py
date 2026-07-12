import os, sys

BASE = "UTan_Flutter"
DIRS = [
    f"{BASE}/lib/models",
    f"{BASE}/lib/services",
    f"{BASE}/lib/providers",
    f"{BASE}/lib/screens",
    f"{BASE}/lib/widgets",
    f"{BASE}/lib/player",
    f"{BASE}/assets/fonts",
    f"{BASE}/assets/images",
]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

def w(rel_path, content):
    full = os.path.join(BASE, rel_path) if not rel_path.startswith(".") else rel_path
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Directories created")

# --- pubspec.yaml ---
_pubspec = "name: utan_flutter\ndescription: UTan Video Streaming App\npublish_to: 'none'\nversion: 5.0.0+5\n\nenvironment:\n  sdk: '>=3.2.0 <4.0.0'\n  flutter: '>=3.22.0'\n\ndependencies:\n  flutter:\n    sdk: flutter\n  provider: ^6.1.2\n  http: ^1.2.1\n  cached_network_image: ^3.3.1\n  shared_preferences: ^2.3.0\n  video_player: ^2.8.6\n  chewie: ^1.8.1\n  intl: ^0.19.0\n  wakelock_plus: ^1.2.8\n  url_launcher: ^6.3.0\n  path_provider: ^2.1.3\n  flutter_cache_manager: ^3.4.1\n  supabase_flutter: ^2.5.3\n  google_sign_in: ^6.2.1\n  app_links: ^6.0.0\n  image_picker: ^1.0.7\n  webview_flutter: ^4.8.0\n  dio: ^5.4.3\n  path_provider: ^2.1.4\n  open_file: ^3.3.2\n  rxdart: ^0.28.0\n\ndev_dependencies:\n  flutter_test:\n    sdk: flutter\n  flutter_lints: ^4.0.0\n  flutter_launcher_icons: ^0.14.1\n\nflutter_icons:\n  android: true\n  ios: false\n  image_path: 'assets/images/app.jpg'\n  adaptive_icon_background: '#0D0D0D'\n  adaptive_icon_foreground: 'assets/images/app.jpg'\n  min_sdk_android: 21\n\nflutter:\n  uses-material-design: true\n\n  assets:\n    - assets/images/\n\n  fonts:\n    - family: Cairo\n      fonts:\n        - asset: assets/fonts/Cairo.ttf\n          weight: 400\n        - asset: assets/fonts/Cairo-Bold-1.ttf\n          weight: 700\n    - family: Rubik\n      fonts:\n        - asset: assets/fonts/Rubik.ttf\n          weight: 400\n        - asset: assets/fonts/Rubik-Bold.ttf\n          weight: 700\n    - family: IBMPlexArabic\n      fonts:\n        - asset: assets/fonts/Ibm.ttf\n          weight: 400\n        - asset: assets/fonts/IBMPlexArabic-Bold.ttf\n          weight: 700\n    - family: ExpoArabic\n      fonts:\n        - asset: assets/fonts/alfont_com_AlFont_com_ExpoArabic-Bold.otf\n          weight: 700\n"
w("pubspec.yaml", _pubspec)
print("pubspec.yaml written")


# --- lib/app_colors.dart ----------------------------------------------------
w("lib/app_colors.dart", r"""import 'package:flutter/material.dart';
import 'app_settings.dart';

// --- Dynamic background based on selected theme --------------------------
Color appBg() {
  switch (AppSettings.instance.appTheme) {
    case 'amoled':
      return Colors.black;
    case 'dark_blue':
      return const Color.fromRGBO(5, 10, 31, 1);
    case 'dark_purple':
      return const Color.fromRGBO(13, 5, 28, 1);
    default:
      return Colors.black;
  }
}

// --- Dynamic accent color -------------------------------------------------
Color utRed() {
  switch (AppSettings.instance.accentColorName) {
    case 'blue':
      return const Color.fromRGBO(26, 102, 230, 1);
    case 'orange':
      return const Color.fromRGBO(242, 115, 13, 1);
    case 'green':
      return const Color.fromRGBO(26, 199, 89, 1);
    case 'pink':
      return const Color.fromRGBO(230, 51, 140, 1);
    default:
      return const Color.fromRGBO(227, 10, 20, 1); // red (default)
  }
}

const Color utWhite = Colors.white;
const Color utSurface = Color(0x1FFFFFFF);

// --- L() localisation helper ---------------------------------------------
String L(String ar, String en) =>
    AppSettings.instance.appLanguage == 'en' ? en : ar;

// --- App Font helper -----------------------------------------------------
TextStyle appFontStyle(double size, {bool bold = false, Color? color}) {
  return TextStyle(
    fontFamily: 'ExpoArabic',
    fontSize: size,
    fontWeight: bold ? FontWeight.w700 : FontWeight.w400,
    color: color ?? Colors.white,
  );
}

TextStyle subtitleFontStyle(String fontName, double size, {Color? color}) {
  String family;
  switch (fontName) {
    case 'IBMPlexArabic': family = 'IBMPlexArabic'; break;
    case 'Rubik':         family = 'Rubik';          break;
    case 'ExpoArabic':    family = 'ExpoArabic';     break;
    case 'Cairo':
    default:              family = 'Cairo';
  }
  return TextStyle(
    fontFamily: family,
    fontSize: size,
    fontWeight: FontWeight.w700,
    color: color ?? Colors.white,
  );
}

// --- Category color/icon helpers -----------------------------------------
Color categoryColor(String nameEn) {
  final n = nameEn.toLowerCase();
  if (n.contains('anime')) return Colors.purple;
  if (n.contains('movie')) return Colors.blue;
  if (n.contains('kids') || n.contains('cartoon')) return Colors.orange;
  if (n.contains('action')) return Colors.red;
  if (n.contains('horror')) return const Color(0xFF800000);
  if (n.contains('comedy')) return Colors.yellow;
  if (n.contains('romance')) return Colors.pink;
  if (n.contains('korean') || n.contains('asian')) return Colors.pink;
  if (n.contains('netflix')) return Colors.red;
  if (n.contains('disney')) return Colors.cyan;
  if (n.contains('ramadan')) return const Color(0xFF997A00);
  if (n.contains('turkish')) return Colors.teal;
  if (n.contains('arabic')) return Colors.amber;
  if (n.contains('marvel')) return Colors.red.shade800;
  if (n.contains('hbo')) return Colors.purple.shade700;
  return utRed();
}

IconData categoryIcon(String nameEn) {
  final n = nameEn.toLowerCase();
  if (n.contains('anime')) return Icons.auto_awesome;
  if (n.contains('movie')) return Icons.movie_filter;
  if (n.contains('series') || n.contains('tv')) return Icons.tv;
  if (n.contains('kids') || n.contains('cartoon')) return Icons.child_care;
  if (n.contains('action')) return Icons.bolt;
  if (n.contains('korean') || n.contains('asian')) return Icons.language;
  if (n.contains('netflix')) return Icons.live_tv;
  if (n.contains('disney')) return Icons.waving_hand;
  if (n.contains('document')) return Icons.article;
  if (n.contains('turkish')) return Icons.nightlight;
  if (n.contains('ramadan')) return Icons.cruelty_free;
  if (n.contains('horror')) return Icons.dark_mode;
  if (n.contains('comedy')) return Icons.sentiment_very_satisfied;
  if (n.contains('romance')) return Icons.favorite;
  if (n.contains('arabic')) return Icons.translate;
  if (n.contains('marvel')) return Icons.shield;
  if (n.contains('hbo')) return Icons.hd;
  return Icons.play_circle_fill;
}

// --- Color from hex --------------------------------------------------------
Color colorFromHex(String hex) {
  final cleaned = hex.replaceAll('#', '');
  if (cleaned.length == 6) {
    return Color(int.parse('FF$cleaned', radix: 16));
  }
  if (cleaned.length == 8) {
    return Color(int.parse(cleaned, radix: 16));
  }
  return Colors.white;
}

String formatTime(double seconds) {
  if (seconds.isNaN || seconds.isInfinite) return '00:00';
  final h = seconds ~/ 3600;
  final m = (seconds % 3600) ~/ 60;
  final s = seconds % 60;
  if (h > 0) {
    return '${h.toString().padLeft(2, '0')}:${m.toString().padLeft(2, '0')}:${s.toInt().toString().padLeft(2, '0')}';
  }
  return '${m.toString().padLeft(2, '0')}:${s.toInt().toString().padLeft(2, '0')}';
}
""")

print("✅ app_colors.dart written")

# --- lib/app_settings.dart -------------------------------------------------
w("lib/app_settings.dart", r"""import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AppSettings extends ChangeNotifier {
  static final AppSettings instance = AppSettings._();
  AppSettings._();

  late SharedPreferences _prefs;

  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  // -- Subtitle settings -------------------------------------------
  double get subtitleFontSize => _prefs.getDouble('sub_fontSize') ?? 22.0;
  set subtitleFontSize(double v) { _prefs.setDouble('sub_fontSize', v); notifyListeners(); }

  String get subtitleColorHex => _prefs.getString('sub_colorHex') ?? '#FFFFFF';
  set subtitleColorHex(String v) { _prefs.setString('sub_colorHex', v); notifyListeners(); }

  double get subtitleBgOpacity => _prefs.getDouble('sub_bgOpacity') ?? 0.6;
  set subtitleBgOpacity(double v) { _prefs.setDouble('sub_bgOpacity', v); notifyListeners(); }

  double get subtitleBottomPad => _prefs.getDouble('sub_bottomPad') ?? 20.0;
  set subtitleBottomPad(double v) { _prefs.setDouble('sub_bottomPad', v); notifyListeners(); }

  bool get subtitleShowShadow => _prefs.getBool('sub_shadow') ?? true;
  set subtitleShowShadow(bool v) { _prefs.setBool('sub_shadow', v); notifyListeners(); }

  bool get subtitleShowStroke => _prefs.getBool('sub_stroke') ?? true;
  set subtitleShowStroke(bool v) { _prefs.setBool('sub_stroke', v); notifyListeners(); }

  bool get subtitlesEnabled => _prefs.getBool('sub_enabled') ?? true;
  set subtitlesEnabled(bool v) { _prefs.setBool('sub_enabled', v); notifyListeners(); }

  String get subtitleFontName => _prefs.getString('sub_fontName') ?? 'Cairo';
  set subtitleFontName(String v) { _prefs.setString('sub_fontName', v); notifyListeners(); }

  double get subtitleDelay => _prefs.getDouble('sub_delay') ?? 0.0;
  set subtitleDelay(double v) { _prefs.setDouble('sub_delay', v); notifyListeners(); }

  // -- Autoplay settings -------------------------------------------
  bool get autoPlayNextEnabled => _prefs.getBool('autoplay_next') ?? true;
  set autoPlayNextEnabled(bool v) { _prefs.setBool('autoplay_next', v); notifyListeners(); }

  int get autoPlayCountdownSeconds => _prefs.getInt('autoplay_countdown') ?? 10;
  set autoPlayCountdownSeconds(int v) { _prefs.setInt('autoplay_countdown', v); notifyListeners(); }

  // -- Quality preference ------------------------------------------
  String get preferredQuality => _prefs.getString('pref_quality') ?? 'auto';
  set preferredQuality(String v) { _prefs.setString('pref_quality', v); notifyListeners(); }

  // -- WiFi-only downloads -----------------------------------------
  bool get downloadOverWifiOnly => _prefs.getBool('download_wifi_only') ?? false;
  set downloadOverWifiOnly(bool v) { _prefs.setBool('download_wifi_only', v); notifyListeners(); }

  // -- Download open mode -------------------------------------------
  // 'internal' = open in app player, 'external' = system browser/downloader
  String get downloadOpenMode => _prefs.getString('download_open_mode') ?? 'external';
  set downloadOpenMode(String v) { _prefs.setString('download_open_mode', v); notifyListeners(); }

  String get downloadPath => _prefs.getString('download_path') ?? '';
  set downloadPath(String v) { _prefs.setString('download_path', v); notifyListeners(); }

  // -- Language ----------------------------------------------------
  String get appLanguage => _prefs.getString('app_language') ?? 'ar';
  set appLanguage(String v) { _prefs.setString('app_language', v); notifyListeners(); }

  // -- Theme --------------------------------------------------------
  String get appTheme => _prefs.getString('app_theme') ?? 'amoled';
  set appTheme(String v) { _prefs.setString('app_theme', v); notifyListeners(); }

  // -- Accent color -------------------------------------------------
  String get accentColorName => _prefs.getString('accent_color') ?? 'red';
  set accentColorName(String v) { _prefs.setString('accent_color', v); notifyListeners(); }

  // -- Grid size ----------------------------------------------------
  String get gridSizeStr => _prefs.getString('grid_size') ?? 'medium';
  set gridSizeStr(String v) { _prefs.setString('grid_size', v); notifyListeners(); }

  double get posterMinWidth {
    switch (gridSizeStr) {
      case 'small': return 90;
      case 'large': return 150;
      default: return 110;
    }
  }

  void clearCache() {
    notifyListeners();
  }
}
""")

print("✅ app_settings.dart written")

# --- lib/models/video_item.dart ----------------------------------------------
w("lib/models/video_item.dart", r"""class VideoItem {
  final String id;
  final String title;
  final String imageUrl;
  final String type;

  const VideoItem({
    required this.id,
    required this.title,
    required this.imageUrl,
    required this.type,
  });

  factory VideoItem.fromJson(Map<String, dynamic> j) => VideoItem(
    id: j['id'] as String? ?? '',
    title: j['title'] as String? ?? '',
    imageUrl: j['image_url'] as String? ?? '',
    type: j['type'] as String? ?? 'post',
  );

  Map<String, dynamic> toJson() => {
    'id': id, 'title': title, 'image_url': imageUrl, 'type': type,
  };

  @override bool operator ==(Object o) => o is VideoItem && o.id == id;
  @override int get hashCode => id.hashCode;
}
""")

# --- lib/models/episode_item.dart -------------------------------------------
w("lib/models/episode_item.dart", r"""class EpisodeItem {
  final String id;
  final String title;
  final String url;
  final String url720;
  final String url1080;
  final String url360;
  final String url4k;
  final String subtitleUrl;
  final String subtitleVttUrl;
  final String season;
  final String imageUrl;

  const EpisodeItem({
    required this.id,
    required this.title,
    required this.url,
    this.url720 = '',
    this.url1080 = '',
    this.url360 = '',
    this.url4k = '',
    this.subtitleUrl = '',
    this.subtitleVttUrl = '',
    this.season = '',
    this.imageUrl = '',
  });

  int? get episodeNumber {
    final rx = RegExp(r'(\d+)');
    final m = rx.firstMatch(title);
    if (m != null) return int.tryParse(m.group(1)!);
    return null;
  }

  @override bool operator ==(Object o) => o is EpisodeItem && o.id == id;
  @override int get hashCode => id.hashCode;
}
""")

# --- lib/models/media_details.dart ------------------------------------------
w("lib/models/media_details.dart", r"""import 'episode_item.dart';

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
  String movieUrl720;
  String movieUrl1080;
  String movieUrl360;
  String movieUrl4k;
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
    this.movieUrl720 = '',
    this.movieUrl1080 = '',
    this.movieUrl360 = '',
    this.movieUrl4k = '',
    this.movieSubtitleUrl = '',
    this.movieSubtitleVttUrl = '',
    this.episodes = const [],
  });

  Map<String, List<EpisodeItem>> get seasonsDict {
    final map = <String, List<EpisodeItem>>{};
    for (final ep in episodes) {
      map.putIfAbsent(ep.season, () => []).add(ep);
    }
    return map;
  }

  List<String> get sortedSeasons {
    return seasonsDict.keys.toList()
      ..sort((a, b) {
        final na = int.tryParse(a.replaceAll(RegExp(r'[^\d]'), '')) ?? 0;
        final nb = int.tryParse(b.replaceAll(RegExp(r'[^\d]'), '')) ?? 0;
        return na.compareTo(nb);
      });
  }

  EpisodeItem? nextEpisode(String episodeId) {
    final idx = episodes.indexWhere((e) => e.id == episodeId);
    if (idx == -1 || idx + 1 >= episodes.length) return null;
    return episodes[idx + 1];
  }

  EpisodeItem? episode(String id) =>
      episodes.where((e) => e.id == id).firstOrNull;
}
""")

# --- lib/models/subtitle_cue.dart -------------------------------------------
w("lib/models/subtitle_cue.dart", r"""class SubtitleCue {
  final double startTime;
  final double endTime;
  final String text;

  const SubtitleCue({
    required this.startTime,
    required this.endTime,
    required this.text,
  });
}
""")

# --- lib/models/watch_progress.dart -----------------------------------------
w("lib/models/watch_progress.dart", r"""class WatchProgress {
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

  double get percent {
    if (durationSeconds <= 0) return 0;
    return (progressSeconds / durationSeconds * 100).clamp(0, 100);
  }

  const WatchProgress({
    required this.itemId,
    required this.title,
    required this.imageUrl,
    required this.episodeId,
    required this.episodeTitle,
    required this.progressSeconds,
    required this.durationSeconds,
    required this.updatedAt,
    this.videoUrl = '',
    this.videoUrl720 = '',
    this.videoUrl1080 = '',
    this.videoUrl360 = '',
    this.videoUrl4k = '',
    this.subtitleUrl = '',
    this.subtitleVttUrl = '',
    this.isMovie = true,
  });

  static String progressKey(String itemId, String episodeId) {
    final eid = episodeId.trim();
    if (eid.isEmpty || eid == itemId) return itemId;
    return '${itemId}__$eid';
  }

  Map<String, dynamic> toJson() => {
    'itemId': itemId, 'title': title, 'imageUrl': imageUrl,
    'episodeId': episodeId, 'episodeTitle': episodeTitle,
    'progressSeconds': progressSeconds, 'durationSeconds': durationSeconds,
    'updatedAt': updatedAt.toIso8601String(),
    'videoUrl': videoUrl, 'videoUrl720': videoUrl720,
    'videoUrl1080': videoUrl1080, 'videoUrl360': videoUrl360,
    'videoUrl4k': videoUrl4k,
    'subtitleUrl': subtitleUrl, 'subtitleVttUrl': subtitleVttUrl,
    'isMovie': isMovie,
  };

  factory WatchProgress.fromJson(Map<String, dynamic> j) => WatchProgress(
    itemId: j['itemId'] as String? ?? '',
    title: j['title'] as String? ?? '',
    imageUrl: j['imageUrl'] as String? ?? '',
    episodeId: j['episodeId'] as String? ?? '',
    episodeTitle: j['episodeTitle'] as String? ?? '',
    progressSeconds: (j['progressSeconds'] as num?)?.toDouble() ?? 0,
    durationSeconds: (j['durationSeconds'] as num?)?.toDouble() ?? 0,
    updatedAt: DateTime.tryParse(j['updatedAt'] as String? ?? '') ?? DateTime.now(),
    videoUrl: j['videoUrl'] as String? ?? '',
    videoUrl720: j['videoUrl720'] as String? ?? '',
    videoUrl1080: j['videoUrl1080'] as String? ?? '',
    videoUrl360: j['videoUrl360'] as String? ?? '',
    videoUrl4k: j['videoUrl4k'] as String? ?? '',
    subtitleUrl: j['subtitleUrl'] as String? ?? '',
    subtitleVttUrl: j['subtitleVttUrl'] as String? ?? '',
    isMovie: j['isMovie'] as bool? ?? true,
  );
}
""")

# --- lib/models/watch_list.dart ---------------------------------------------
w("lib/models/download_item.dart", r"""import 'dart:convert';

enum DownloadStatus { queued, downloading, completed, failed, cancelled }

class DownloadItem {
  final String id;
  final String itemId;
  final String episodeId;
  final String title;
  final String imageUrl;
  final String url;
  String filePath;
  DownloadStatus status;
  double progress;
  int totalBytes;
  int downloadedBytes;
  final DateTime addedAt;

  DownloadItem({
    required this.id, required this.itemId, required this.episodeId,
    required this.title, required this.imageUrl, required this.url,
    this.filePath = '', this.status = DownloadStatus.queued,
    this.progress = 0, this.totalBytes = 0, this.downloadedBytes = 0,
    DateTime? addedAt,
  }) : addedAt = addedAt ?? DateTime.now();

  bool get isMovie => episodeId == itemId;

  Map<String, dynamic> toJson() => {
    'id': id, 'itemId': itemId, 'episodeId': episodeId,
    'title': title, 'imageUrl': imageUrl, 'url': url,
    'filePath': filePath, 'status': status.name,
    'progress': progress, 'totalBytes': totalBytes,
    'downloadedBytes': downloadedBytes,
    'addedAt': addedAt.toIso8601String(),
  };

  factory DownloadItem.fromJson(Map<String, dynamic> j) => DownloadItem(
    id: j['id'] as String, itemId: j['itemId'] as String,
    episodeId: j['episodeId'] as String, title: j['title'] as String,
    imageUrl: j['imageUrl'] as String? ?? '', url: j['url'] as String,
    filePath: j['filePath'] as String? ?? '',
    status: DownloadStatus.values.firstWhere(
        (s) => s.name == j['status'], orElse: () => DownloadStatus.queued),
    progress: (j['progress'] as num?)?.toDouble() ?? 0,
    totalBytes: j['totalBytes'] as int? ?? 0,
    downloadedBytes: j['downloadedBytes'] as int? ?? 0,
    addedAt: DateTime.tryParse(j['addedAt'] as String? ?? '') ?? DateTime.now(),
  );
}
""")
print("✅ download_item.dart written")


# --- lib/models/watch_list.dart ---------------------------------------------
w("lib/models/watch_list.dart", r"""import 'dart:convert';
import 'video_item.dart';

class WatchListItem {
  final String id;
  final String title;
  final String imageUrl;
  final String type;
  final DateTime addedAt;

  WatchListItem.fromVideo(VideoItem v)
      : id = v.id,
        title = v.title,
        imageUrl = v.imageUrl,
        type = v.type,
        addedAt = DateTime.now();

  WatchListItem({
    required this.id, required this.title,
    required this.imageUrl, required this.type,
    required this.addedAt,
  });

  Map<String, dynamic> toJson() => {
    'id': id, 'title': title, 'imageUrl': imageUrl,
    'type': type, 'addedAt': addedAt.toIso8601String(),
  };

  factory WatchListItem.fromJson(Map<String, dynamic> j) => WatchListItem(
    id: j['id'] as String, title: j['title'] as String,
    imageUrl: j['imageUrl'] as String, type: j['type'] as String,
    addedAt: DateTime.tryParse(j['addedAt'] as String? ?? '') ?? DateTime.now(),
  );

  @override bool operator ==(Object o) => o is WatchListItem && o.id == id;
  @override int get hashCode => id.hashCode;
}

class WatchList {
  String id;
  String name;
  bool isPrivate;
  List<WatchListItem> items;
  DateTime createdAt;

  WatchList({
    required this.id, required this.name,
    this.isPrivate = true,
    this.items = const [],
    DateTime? createdAt,
  }) : createdAt = createdAt ?? DateTime.now();

  List<String> get posterUrls => items.take(4).map((i) => i.imageUrl).toList();

  Map<String, dynamic> toJson() => {
    'id': id, 'name': name, 'isPrivate': isPrivate,
    'items': items.map((i) => i.toJson()).toList(),
    'createdAt': createdAt.toIso8601String(),
  };

  factory WatchList.fromJson(Map<String, dynamic> j) => WatchList(
    id: j['id'] as String, name: j['name'] as String,
    isPrivate: j['isPrivate'] as bool? ?? true,
    items: (j['items'] as List<dynamic>? ?? [])
        .map((e) => WatchListItem.fromJson(e as Map<String, dynamic>))
        .toList(),
    createdAt: DateTime.tryParse(j['createdAt'] as String? ?? '') ?? DateTime.now(),
  );
}
""")

# --- lib/models/site_category.dart ------------------------------------------
w("lib/models/site_category.dart", r"""class SiteCategory {
  final int id;
  final int remoteId;
  final bool isTag;
  final String nameAr;
  final String nameEn;

  const SiteCategory({
    required this.id,
    int? remoteId,
    this.isTag = false,
    required this.nameAr,
    required this.nameEn,
  }) : remoteId = remoteId ?? id;

  String localizedName(String lang) => lang == 'en' ? nameEn : nameAr;
}

const List<SiteCategory> siteCategories = [
  SiteCategory(id: 1,    nameAr: 'مسلسلات أجنبية',        nameEn: 'Foreign Series'),
  SiteCategory(id: 2,    nameAr: 'مسلسلات عربية',         nameEn: 'Arabic Series'),
  SiteCategory(id: 3,    nameAr: 'أنمي مدبلج عربي',       nameEn: 'Arabic Dubbed Anime'),
  SiteCategory(id: 4,    nameAr: 'أنمي مترجم',            nameEn: 'Subbed Anime'),
  SiteCategory(id: 5,    nameAr: 'أفلام بوليوود',         nameEn: 'Bollywood Movies'),
  SiteCategory(id: 6,    nameAr: 'مسلسلات هندية',         nameEn: 'Indian Series'),
  SiteCategory(id: 7,    nameAr: 'أفلام عربية',           nameEn: 'Arabic Movies'),
  SiteCategory(id: 8,    nameAr: 'مسلسلات بوليوود',       nameEn: 'Bollywood Series'),
  SiteCategory(id: 9,    nameAr: 'أفلام أنمي',            nameEn: 'Anime Movies'),
  SiteCategory(id: 10,   nameAr: 'أفلام مكتب الصندوق',    nameEn: 'US Box Office'),
  SiteCategory(id: 13,   nameAr: 'سينما عربية',           nameEn: 'Arabic Cinemas'),
  SiteCategory(id: 14,   nameAr: 'أفلام تركية',           nameEn: 'Turkish Movies'),
  SiteCategory(id: 15,   nameAr: 'مسلسلات تركية',         nameEn: 'Turkish Series'),
  SiteCategory(id: 16,   nameAr: 'أفلام كرتون',           nameEn: 'Cartoon Movies'),
  SiteCategory(id: 17,   nameAr: 'مسلسلات كرتون',         nameEn: 'Cartoon Series'),
  SiteCategory(id: 18,   nameAr: 'أفلام أجنبية',          nameEn: 'Foreign Movies'),
  SiteCategory(id: 20,   nameAr: 'مسلسلات مدبلجة عربي',   nameEn: 'Arabic Dubbed Series'),
  SiteCategory(id: 21,   nameAr: 'أفلام مدبلجة عربي',    nameEn: 'Arabic Dubbed Movies'),
  SiteCategory(id: 1014, nameAr: 'أفلام كردية',           nameEn: 'Kurdish Movies'),
  SiteCategory(id: 1015, nameAr: 'مسلسلات كردية',         nameEn: 'Kurdish Series'),
  SiteCategory(id: 1022, nameAr: 'أنمي عربي',             nameEn: 'Arabic Anime'),
  SiteCategory(id: 1029, nameAr: 'أنمي مدبلج إنجليزي',   nameEn: 'English Dubbed Anime'),
  SiteCategory(id: 44,  remoteId: 44,  isTag: true, nameAr: 'نيتفلكس',          nameEn: 'Netflix'),
  SiteCategory(id: 9014, remoteId: 14, isTag: true, nameAr: 'عالم مارفل',        nameEn: 'Marvel'),
  SiteCategory(id: 73,  remoteId: 73,  isTag: true, nameAr: 'اتش بي او ماكس',   nameEn: 'HBO Max'),
  SiteCategory(id: 72,  remoteId: 72,  isTag: true, nameAr: 'ديزني',             nameEn: 'Disney+'),
  SiteCategory(id: 9018, remoteId: 18, isTag: true, nameAr: 'للاطفال',           nameEn: 'For KIDS'),
];
""")

# --- lib/models/feedback_item.dart ------------------------------------------
w("lib/models/feedback_item.dart", r"""class FeedbackItem {
  final String id;
  final String userId;
  final String displayName;
  final String? email;
  final String type;
  final String message;
  final String status;
  final String createdAt;

  const FeedbackItem({
    required this.id, required this.userId, required this.displayName,
    this.email, required this.type, required this.message,
    required this.status, required this.createdAt,
  });

  bool get isComplaint => type == 'complaint';

  factory FeedbackItem.fromJson(Map<String, dynamic> j) => FeedbackItem(
    id: j['id'] as String, userId: j['user_id'] as String,
    displayName: j['display_name'] as String, email: j['email'] as String?,
    type: j['type'] as String, message: j['message'] as String,
    status: j['status'] as String? ?? 'open',
    createdAt: j['created_at'] as String? ?? '',
  );
}
""")

# --- lib/models/comment_item.dart -------------------------------------------
w("lib/models/comment_item.dart", r"""class CommentItem {
  final String id;
  final String itemId;
  final String userId;
  final String displayName;
  final String text;
  final String createdAt;

  const CommentItem({
    required this.id, required this.itemId, required this.userId,
    required this.displayName, required this.text, required this.createdAt,
  });

  factory CommentItem.fromJson(Map<String, dynamic> j) => CommentItem(
    id: j['id'] as String, itemId: j['item_id'] as String,
    userId: j['user_id'] as String, displayName: j['display_name'] as String,
    text: j['text'] as String, createdAt: j['created_at'] as String? ?? '',
  );
}
""")

print("✅ All model files written")

# --- lib/services/scraper.dart -----------------------------------------------
w("lib/services/scraper.dart", r"""import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/video_item.dart';
import '../models/media_details.dart';
import '../models/episode_item.dart';

const String _baseUrl = 'https://movie.vodu.me/';
const String _userAgent =
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36';

String _optimizeImageUrl(String url, {int w = 400, int h = 600}) {
  if (url.contains('w=750') || url.contains('h=388')) return url;
  final sep = url.contains('?') ? '&' : '?';
  return '$url${sep}w=$w&h=$h&crop-to-fit';
}

String _fixUrl(String u) {
  if (u.isEmpty) return '';
  if (u.startsWith('http')) return u;
  return '$_baseUrl$u';
}

class MovieScraper extends ChangeNotifier {
  List<VideoItem> heroItems = [];
  List<({String name, List<VideoItem> items, int tagId})> categories = [];
  List<VideoItem> allItemsPool = [];
  bool isLoading = false;

  Future<void> fetchHome() async {
    isLoading = true;
    notifyListeners();
    try {
      final resp = await http.get(
        Uri.parse('${_baseUrl}index.php'),
        headers: {'User-Agent': _userAgent},
      ).timeout(const Duration(seconds: 20));
      if (resp.statusCode == 200) {
        final html = resp.body;
        final result = await compute(_parseHomePage, html);
        heroItems = result.$1;
        final filtered = result.$2.where((s) => s.name.toLowerCase() != 'featured').toList();
        categories = filtered;
        allItemsPool = filtered.expand((s) => s.items).toList();
      }
    } catch (_) {}
    isLoading = false;
    notifyListeners();
  }

  Future<void> refreshHome() async => fetchHome();

  Future<List<VideoItem>> fetchCategory(
    int typeId, {
    int page = 1,
    bool useTag = false,
    String sort = 'date',
    String? genre,
  }) async {
    final pageParam = page > 1 ? '&page=$page' : '';
    var urlStr = useTag
        ? '${_baseUrl}index.php?do=list&tag=$typeId$pageParam'
        : '${_baseUrl}index.php?do=list&type=$typeId$pageParam';
    if (sort.isNotEmpty) urlStr += '&sort=$sort';
    if (genre != null && genre.isNotEmpty) urlStr += '&genre=$genre';
    try {
      final resp = await http.get(
        Uri.parse(urlStr),
        headers: {'User-Agent': _userAgent},
      ).timeout(const Duration(seconds: 20));
      if (resp.statusCode == 200) {
        return await compute(_parseListPage, resp.body);
      }
    } catch (_) {}
    return [];
  }

  Future<bool> hasMorePages(String html, int currentPage) async {
    return compute(_detectHasMore, (html, currentPage));
  }

  Future<List<VideoItem>> advancedSearch({
    String? title,
    String? genre,
    String? type,
    String? year,
    String? language,
    String? director,
    String? imdbrate,
  }) async {
    final params = <String, String>{'do': 'list'};
    if (title != null && title.isNotEmpty) params['title'] = title;
    if (genre != null && genre.isNotEmpty) params['genre'] = genre;
    if (type != null && type.isNotEmpty) params['type'] = type;
    if (year != null && year.isNotEmpty) params['year'] = year;
    if (language != null && language.isNotEmpty) params['language'] = language;
    if (director != null && director.isNotEmpty) params['director'] = director;
    if (imdbrate != null && imdbrate.isNotEmpty) params['imdbrate'] = imdbrate;
    final uri = Uri.parse(_baseUrl + 'index.php').replace(queryParameters: params);
    try {
      final resp = await http.get(uri, headers: {'User-Agent': _userAgent})
          .timeout(const Duration(seconds: 20));
      if (resp.statusCode == 200) {
        return await compute(_parseListPage, resp.body);
      }
    } catch (_) {}
    return [];
  }

  Future<List<VideoItem>> searchItems(String query) async {
    if (query.trim().isEmpty) return [];
    final params = <String, String>{'do': 'list', 'title': query.trim()};
    final uri = Uri.parse(_baseUrl + 'index.php').replace(queryParameters: params);
    try {
      final resp = await http.get(uri, headers: {'User-Agent': _userAgent})
          .timeout(const Duration(seconds: 20));
      if (resp.statusCode == 200) {
        return await compute(_parseListPage, resp.body);
      }
    } catch (_) {}
    return [];
  }

  Future<MediaDetails> fetchDetails(String id) async {
    try {
      final resp = await http.get(
        Uri.parse('${_baseUrl}index.php?do=view&type=post&id=$id'),
        headers: {'User-Agent': _userAgent},
      ).timeout(const Duration(seconds: 25));
      if (resp.statusCode == 200) {
        return await compute(_parseDetails, resp.body);
      }
    } catch (_) {}
    return MediaDetails();
  }
}

// -- Isolate-safe parsers ----------------------------------------------------

(List<VideoItem>, List<({String name, List<VideoItem> items, int tagId})>)
    _parseHomePage(String html) {
  final carouselItems = <VideoItem>[];
  final carRx = RegExp(
    r'<a href="index\.php\?do=view&type=post&id=(\d+)"><img src="([^"]+)"[^>]*alt="([^"]*)">');
  for (final m in carRx.allMatches(html)) {
    final id = m.group(1)!;
    var img = m.group(2)!;
    final title = m.group(3)!;
    if (!img.startsWith('http')) img = _baseUrl + img;
    if (!carouselItems.any((e) => e.id == id)) {
      carouselItems.add(VideoItem(id: id, title: title, imageUrl: img, type: 'post'));
    }
  }

  final sections = <({String name, List<VideoItem> items, int tagId})>[];
  final headerRx = RegExp(r'<h2><a href="\?do=list&tag=(\d+)"[^>]*>([^<]+)</a></h2>');
  final itemRx = RegExp(
    r'<a href="index\.php\?do=view&type=post&id=(\d+)">\s*<img src="([^"]+)"[^>]*>\s*<div class="mytitle">([^<]*)</div>',
    dotAll: true,
  );

  final headerMatches = headerRx.allMatches(html).toList();
  for (int i = 0; i < headerMatches.length; i++) {
    final hm = headerMatches[i];
    final tagId = int.tryParse(hm.group(1)!) ?? -1;
    final sectionName = hm.group(2)!.trim();
    final blockStart = hm.end;
    final blockEnd = i + 1 < headerMatches.length ? headerMatches[i + 1].start : html.length;
    final block = html.substring(blockStart, blockEnd);
    final items = <VideoItem>[];
    for (final m in itemRx.allMatches(block)) {
      final id = m.group(1)!;
      var img = m.group(2)!;
      final t = m.group(3)!.trim();
      if (!img.startsWith('http')) img = _baseUrl + img;
      img = _optimizeImageUrl(img);
      if (!items.any((e) => e.id == id)) {
        items.add(VideoItem(id: id, title: t, imageUrl: img, type: 'post'));
      }
    }
    if (items.isNotEmpty) {
      sections.add((name: sectionName, items: items, tagId: tagId));
    }
  }
  return (carouselItems, sections);
}

List<VideoItem> _parseListPage(String html) {
  final items = <VideoItem>[];
  final rx = RegExp(
    r'href="index\.php\?do=view&type=post&id=(\d+)"><img src="([^"]+)"[^>]*>\s*</a>\s*<div class="mytitle">\s*<a[^>]*>([^<]+)</a>',
    dotAll: true,
  );
  for (final m in rx.allMatches(html)) {
    final id = m.group(1)!;
    var img = m.group(2)!;
    final title = m.group(3)!.trim();
    if (!img.startsWith('http')) img = _baseUrl + img;
    if (!items.any((e) => e.id == id)) {
      items.add(VideoItem(id: id, title: title, imageUrl: _optimizeImageUrl(img), type: 'post'));
    }
  }
  return items;
}

bool _detectHasMore((String, int) args) {
  final html = args.$1;
  final currentPage = args.$2;
  final paginationStart = html.indexOf('<ul class="pagination">');
  if (paginationStart == -1) return false;
  final paginationEnd = html.indexOf('</ul>', paginationStart);
  if (paginationEnd == -1) return false;
  final block = html.substring(paginationStart, paginationEnd);
  final rx = RegExp(r'page=(\d+)');
  final pages = rx.allMatches(block)
      .map((m) => int.tryParse(m.group(1)!) ?? 0)
      .toList();
  final maxPage = pages.isEmpty ? 0 : pages.reduce((a, b) => a > b ? a : b);
  return maxPage > currentPage;
}

MediaDetails _parseDetails(String html) {
  final d = MediaDetails();

  String? first(String pattern, {bool dotAll = false}) {
    final rx = RegExp(pattern, dotAll: dotAll);
    final m = rx.firstMatch(html);
    if (m != null && m.groupCount >= 1) return m.group(1)?.trim();
    return null;
  }

  d.title   = first(r'<h1>(.*?)</h1>') ?? '';
  d.year    = first(r'<span>Year:\s*</span>\s*([^<]+)') ?? '';
  d.genre   = first(r'<span>Genre:\s*</span>\s*([^<]+)') ?? '';
  d.rating  = first(r'<span>IMdB Rating:\s*</span>\s*([^<]+)') ?? '';
  d.runtime = first(r'<span>Runtime:\s*</span>\s*([^<]+)') ?? '';
  d.synopsis = first(r'<h3>Synopsis:</h3>.*?<h4>(.*?)</h4>', dotAll: true) ?? '';

  final imgM = RegExp(r'<img src="([^"]+)" class="img-responsive"').firstMatch(html);
  if (imgM != null) {
    var img = imgM.group(1)!;
    if (!img.startsWith('http')) img = _baseUrl + img;
    d.imageUrl = _optimizeImageUrl(img, w: 800, h: 1200);
  }

  final episodes = <EpisodeItem>[];
  final epBlockRx = RegExp(r'<li class="episodeitem">(.*?)</li>', dotAll: true);
  String extract(String pattern, String text) {
    final m = RegExp(pattern).firstMatch(text);
    return m?.group(1)?.trim() ?? '';
  }
  for (final bm in epBlockRx.allMatches(html)) {
    final block = bm.group(1)!;
    final epId  = extract(r'data-id="(\d+)"', block);
    if (epId.isEmpty) continue;
    final epTitle = extract(r'data-title="([^"]*)"', block);
    final epUrl   = extract(r'data-url="([^"]*)"', block);
    if (epUrl.isEmpty) continue;
    // Auto-detect season from title: S01E01, S1E1, الموسم 1, Season 1
    String epSeason = '';
    final sMatch = RegExp(r'[Ss](\d{1,2})[Ee]\d{1,3}').firstMatch(epTitle);
    if (sMatch != null) {
      epSeason = 'S${sMatch.group(1)!.padLeft(2, '0')}';
    } else {
      final arMatch = RegExp(r'الموسم\s*(\d+)').firstMatch(epTitle);
      if (arMatch != null) epSeason = 'S${arMatch.group(1)!.padLeft(2, '0')}';
      else {
        final enMatch = RegExp(r'[Ss]eason\s*(\d+)').firstMatch(epTitle);
        if (enMatch != null) epSeason = 'S${enMatch.group(1)!.padLeft(2, '0')}';
      }
    }
    episodes.add(EpisodeItem(
      id: epId,
      title: epTitle.isEmpty ? 'الحلقة ${episodes.length + 1}' : epTitle,
      url:     epUrl,
      url720:  extract(r'data-url720="([^"]*)"', block),
      url1080: extract(r'data-url1080="([^"]*)"', block),
      url360:  extract(r'data-url360="([^"]*)"', block),
      url4k:   extract(r'data-url4k="([^"]*)"', block),
      subtitleUrl:    extract(r'data-srt="([^"]*)"', block),
      subtitleVttUrl: extract(r'data-webvtt="([^"]*)"', block),
      season: epSeason,
    ));
  }

  if (episodes.isEmpty) {
    d.isMovie = true;
    final movieRx = RegExp(
      r'data-url="([^"]+)"[^>]*data-url360="([^"]*)"[^>]*(?:data-url4k="([^"]*)"[^>]*)?(?:data-url720="([^"]*)"[^>]*)?data-url1080="([^"]*)"[^>]*data-srt="([^"]*)"[^>]*data-webvtt="([^"]*)"',
      dotAll: true,
    );
    final mm = movieRx.firstMatch(html);
    if (mm != null) {
      d.movieUrl         = mm.group(1) ?? '';
      d.movieUrl360      = mm.group(2) ?? '';
      d.movieUrl4k       = mm.group(3) ?? '';
      d.movieUrl720      = mm.group(4) ?? '';
      d.movieUrl1080     = mm.group(5) ?? '';
      d.movieSubtitleUrl    = mm.group(6) ?? '';
      d.movieSubtitleVttUrl = mm.group(7) ?? '';
    }
  } else {
    d.isMovie  = false;
    d.episodes = episodes;
  }
  return d;
}
""")

print("✅ scraper.dart written")

# --- lib/services/subtitle_parser.dart -------------------------------------
w("lib/services/subtitle_parser.dart", r"""import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/subtitle_cue.dart';

class SubtitleParser {
  // Strip subtitle format/style tags: {ut8}, {/ut8}, {bold}, <b>, \N, etc.
  static String _clean(String t) => t
      .replaceAll(RegExp(r'\{[^}]*\}'), '')      // {tag}
      .replaceAll(RegExp(r'<[^>]+>'), '')          // <html>
      .replaceAll(r'\N', '\n')                   // ass newline
      .replaceAll(r'\n', '\n')
      .trim();

  static Future<List<SubtitleCue>> parse(String url) async {
    if (url.isEmpty) return [];
    var clean = url;
    if (!clean.startsWith('http')) clean = 'https://movie.vodu.me/$clean';
    try {
      final resp = await http.get(Uri.parse(url))
          .timeout(const Duration(seconds: 15));
      if (resp.statusCode != 200) return [];
      // Force UTF-8 decode to fix Arabic garbling
      final text = utf8.decode(resp.bodyBytes, allowMalformed: true);
      if (text.contains('WEBVTT')) return _parseWebVTT(text);
      return _parseSRT(text);
    } catch (_) {
      return [];
    }
  }

  static List<SubtitleCue> _parseSRT(String content) {
    final cues = <SubtitleCue>[];
    final normalized = content.replaceAll('\r\n', '\n').replaceAll('\r', '\n');
    final blocks = normalized.split('\n\n');
    for (final block in blocks) {
      final lines = block.split('\n').map((l) => l.trim()).where((l) => l.isNotEmpty).toList();
      if (lines.length < 3) continue;
      final timeLine = lines[1];
      final textParts = lines.sublist(2);
      final text = _clean(textParts.join('\n'));
      if (text.isEmpty) continue;
      final times = timeLine.split(' --> ');
      if (times.length != 2) continue;
      final start = _parseSRTTime(times[0]);
      final end = _parseSRTTime(times[1]);
      if (start == null || end == null) continue;
      cues.add(SubtitleCue(startTime: start, endTime: end, text: text));
    }
    return cues;
  }

  static double? _parseSRTTime(String s) {
    s = s.trim();
    final parts = s.split(',');
    if (parts.length != 2) return null;
    final ms = double.tryParse(parts[1]);
    if (ms == null) return null;
    final timeParts = parts[0].split(':');
    if (timeParts.length != 3) return null;
    final h = double.tryParse(timeParts[0]) ?? 0;
    final m = double.tryParse(timeParts[1]) ?? 0;
    final sec = double.tryParse(timeParts[2]) ?? 0;
    return h * 3600 + m * 60 + sec + ms / 1000;
  }

  static List<SubtitleCue> _parseWebVTT(String content) {
    final cues = <SubtitleCue>[];
    final lines = content.split('\n');
    int i = 0;
    while (i < lines.length) {
      final line = lines[i].trim();
      if (line.contains('-->')) {
        var timePart = line;
        for (final attr in [' position:', ' align:', ' line:', ' size:', ' region:']) {
          timePart = timePart.split(attr)[0];
        }
        final times = timePart.split('-->');
        if (times.length == 2) {
          final start = _parseVTTTime(times[0]);
          final end = _parseVTTTime(times[1]);
          if (start != null && end != null) {
            final textLines = <String>[];
            i++;
            while (i < lines.length && lines[i].trim().isNotEmpty) {
              textLines.add(lines[i].trim());
              i++;
            }
            final text = _clean(textLines.join('\n'));
            if (text.isNotEmpty) {
              cues.add(SubtitleCue(startTime: start, endTime: end, text: text));
            }
            continue;
          }
        }
      }
      i++;
    }
    return cues;
  }

  static double? _parseVTTTime(String s) {
    s = s.trim();
    final parts = s.split(':');
    double hours = 0, minutes = 0, seconds = 0;
    if (parts.length == 3) {
      hours = double.tryParse(parts[0]) ?? 0;
      minutes = double.tryParse(parts[1]) ?? 0;
      final secParts = parts[2].split('.');
      seconds = double.tryParse(secParts[0]) ?? 0;
      if (secParts.length == 2) seconds += (double.tryParse(secParts[1]) ?? 0) / 1000;
    } else if (parts.length == 2) {
      minutes = double.tryParse(parts[0]) ?? 0;
      final secParts = parts[1].split('.');
      seconds = double.tryParse(secParts[0]) ?? 0;
      if (secParts.length == 2) seconds += (double.tryParse(secParts[1]) ?? 0) / 1000;
    } else {
      return null;
    }
    return hours * 3600 + minutes * 60 + seconds;
  }
}
""")

# --- lib/services/auth_session.dart -----------------------------------------
w("lib/services/auth_session.dart", r"""import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SupabaseUser {
  final String id;
  final String? email;
  Map<String, dynamic> userMetadata;
  String avatarUrl;

  SupabaseUser({required this.id, this.email, required this.userMetadata, this.avatarUrl = ''});

  String get displayName {
    final v = userMetadata['display_name'] as String?;
    if (v != null && v.isNotEmpty) return v;
    return email?.split('@').first ?? 'مستخدم';
  }

  void updateDisplayName(String name) {
    userMetadata = Map.from(userMetadata)..['display_name'] = name;
  }

  factory SupabaseUser.fromJson(Map<String, dynamic> j) => SupabaseUser(
    id: j['id'] as String? ?? '',
    email: j['email'] as String?,
    userMetadata: (j['user_metadata'] as Map<String, dynamic>?) ?? {},
    avatarUrl: j['avatar_url'] as String? ?? '',
  );

  Map<String, dynamic> toJson() => {
    'id': id, 'email': email, 'user_metadata': userMetadata, 'avatar_url': avatarUrl,
  };
}

class AuthSession extends ChangeNotifier {
  static final AuthSession instance = AuthSession._();
  AuthSession._();

  SupabaseUser? _user;
  String? _accessToken;
  String? _refreshToken;
  bool _isAdmin = false;

  SupabaseUser? get user => _user;
  String? get accessToken => _accessToken;
  bool get isLoggedIn => _user != null && _accessToken != null;
  bool get isAdmin => _isAdmin;

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _accessToken = prefs.getString('ut_access_token');
    _refreshToken = prefs.getString('ut_refresh_token');
    final userData = prefs.getString('ut_user');
    if (userData != null) {
      try {
        _user = SupabaseUser.fromJson(jsonDecode(userData) as Map<String, dynamic>);
      } catch (_) {}
    }
    notifyListeners();
  }

  Future<void> save({
    required String accessToken,
    required String refreshToken,
    required SupabaseUser user,
  }) async {
    _accessToken = accessToken;
    _refreshToken = refreshToken;
    _user = user;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('ut_access_token', accessToken);
    await prefs.setString('ut_refresh_token', refreshToken);
    await prefs.setString('ut_user', jsonEncode(user.toJson()));
    notifyListeners();
  }

  void setAdmin(bool v) { _isAdmin = v; notifyListeners(); }

  Future<void> updateAvatarUrl(String url) async {
    if (_user == null) return;
    _user = SupabaseUser(
      id: _user!.id, email: _user!.email,
      userMetadata: _user!.userMetadata, avatarUrl: url,
    );
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('ut_user', jsonEncode(_user!.toJson()));
    notifyListeners();
  }

  Future<void> updateDisplayNameLocal(String name) async {
    if (_user == null) return;
    _user!.updateDisplayName(name);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('ut_user', jsonEncode(_user!.toJson()));
    notifyListeners();
  }

  Future<void> signOut() async {
    _user = null;
    _accessToken = null;
    _refreshToken = null;
    _isAdmin = false;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('ut_access_token');
    await prefs.remove('ut_refresh_token');
    await prefs.remove('ut_user');
    notifyListeners();
  }
}
""")

print("✅ subtitle_parser + auth_session written")

# --- lib/services/supabase_manager.dart -------------------------------------
w("lib/services/supabase_manager.dart", r"""import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import '../models/video_item.dart';
import '../models/watch_progress.dart';
import '../models/feedback_item.dart';
import '../models/comment_item.dart';
import 'auth_session.dart';

const _supabaseUrl = 'https://foygwdvggwmmzfbeoone.supabase.co';
const _anonKey =
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZveWd3ZHZnZ3dtbXpmYmVvb25lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE5NjUzMjksImV4cCI6MjA5NzU0MTMyOX0.C8yY99ZUU841rTTQz-yyC1Hvz-hHu4sNKEFSsFTdgS0';

class SupabaseManager {
  static final SupabaseManager instance = SupabaseManager._();
  SupabaseManager._();

  Map<String, String> _baseHeaders({String? token}) => {
    'Content-Type': 'application/json',
    'apikey': _anonKey,
    if (token != null) 'Authorization': 'Bearer $token',
  };

  // -- OAuth ---------------------------------------------------------------
  String getOAuthUrl(String provider) =>
    '$_supabaseUrl/auth/v1/authorize?provider=$provider&redirect_to=utan://';

  Future<Map<String, dynamic>?> getUserFromToken(String token) async {
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/auth/v1/user'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) return jsonDecode(resp.body) as Map<String, dynamic>;
    } catch (_) {}
    return null;
  }

  // -- Auth ----------------------------------------------------------------
  Future<Map<String, dynamic>?> signUp({
    required String email,
    required String password,
    required String displayName,
  }) async {
    try {
      final resp = await http.post(
        Uri.parse('$_supabaseUrl/auth/v1/signup'),
        headers: _baseHeaders(),
        body: jsonEncode({
          'email': email,
          'password': password,
          'data': {'display_name': displayName},
        }),
      ).timeout(const Duration(seconds: 20));
      final body = jsonDecode(resp.body) as Map<String, dynamic>;
      if (resp.statusCode == 200 && body['access_token'] != null) return body;
      return {'error': body['error_description'] ?? body['msg'] ?? body['message'] ?? 'خطأ'};
    } catch (e) {
      return {'error': e.toString()};
    }
  }

  Future<Map<String, dynamic>?> signIn({
    required String email,
    required String password,
  }) async {
    try {
      final resp = await http.post(
        Uri.parse('$_supabaseUrl/auth/v1/token?grant_type=password'),
        headers: _baseHeaders(),
        body: jsonEncode({'email': email, 'password': password}),
      ).timeout(const Duration(seconds: 20));
      final body = jsonDecode(resp.body) as Map<String, dynamic>;
      if (resp.statusCode == 200 && body['access_token'] != null) return body;
      return {'error': body['error_description'] ?? body['msg'] ?? body['message'] ?? 'خطأ'};
    } catch (e) {
      return {'error': e.toString()};
    }
  }

  Future<Map<String, dynamic>?> signInWithGoogle({required String idToken}) async {
    try {
      final resp = await http.post(
        Uri.parse('$_supabaseUrl/auth/v1/token?grant_type=id_token'),
        headers: _baseHeaders(),
        body: jsonEncode({'provider': 'google', 'id_token': idToken}),
      ).timeout(const Duration(seconds: 20));
      final body = jsonDecode(resp.body) as Map<String, dynamic>;
      if (resp.statusCode == 200 && body['access_token'] != null) return body;
      return {'error': body['error_description'] ?? body['msg'] ?? body['message'] ?? 'Google Sign-In failed'};
    } catch (e) {
      return {'error': e.toString()};
    }
  }

  // -- Favorites ----------------------------------------------------------
  Future<List<VideoItem>> fetchFavorites() async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return [];
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/rest/v1/user_favorites?user_id=eq.$userId&select=*'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) {
        final rows = jsonDecode(resp.body) as List<dynamic>;
        return rows.map((r) => VideoItem(
          id: r['item_id'] as String,
          title: r['title'] as String,
          imageUrl: r['image_url'] as String,
          type: r['type'] as String? ?? 'post',
        )).toList();
      }
    } catch (_) {}
    return [];
  }

  Future<bool> upsertFavorite(VideoItem item) async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final resp = await http.post(
        Uri.parse('$_supabaseUrl/rest/v1/user_favorites'),
        headers: {..._baseHeaders(token: token), 'Prefer': 'resolution=merge-duplicates'},
        body: jsonEncode({
          'user_id': userId, 'item_id': item.id,
          'title': item.title, 'image_url': item.imageUrl, 'type': item.type,
        }),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  Future<bool> deleteFavorite(String itemId) async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final resp = await http.delete(
        Uri.parse('$_supabaseUrl/rest/v1/user_favorites?user_id=eq.$userId&item_id=eq.$itemId'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  // -- Watch Progress -----------------------------------------------------
  Future<List<WatchProgress>> fetchProgress() async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return [];
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/rest/v1/user_progress?user_id=eq.$userId&select=*'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) {
        final rows = jsonDecode(resp.body) as List<dynamic>;
        return rows.map((r) => WatchProgress(
          itemId: r['item_id'] as String,
          title: r['title'] as String? ?? '',
          imageUrl: r['image_url'] as String? ?? '',
          episodeId: r['episode_id'] as String? ?? '',
          episodeTitle: r['episode_title'] as String? ?? '',
          progressSeconds: (r['progress_seconds'] as num?)?.toDouble() ?? 0,
          durationSeconds: (r['duration_seconds'] as num?)?.toDouble() ?? 0,
          updatedAt: DateTime.tryParse(r['updated_at'] as String? ?? '') ?? DateTime.now(),
          videoUrl: r['video_url'] as String? ?? '',
          videoUrl720: r['video_url_720'] as String? ?? '',
          videoUrl1080: r['video_url_1080'] as String? ?? '',
          videoUrl360: r['video_url_360'] as String? ?? '',
          videoUrl4k: r['video_url_4k'] as String? ?? '',
          subtitleUrl: r['subtitle_url'] as String? ?? '',
          subtitleVttUrl: r['subtitle_vtt_url'] as String? ?? '',
          isMovie: r['is_movie'] as bool? ?? true,
        )).toList();
      }
    } catch (_) {}
    return [];
  }

  Future<bool> upsertProgress(WatchProgress p) async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final resp = await http.post(
        Uri.parse('$_supabaseUrl/rest/v1/user_progress'),
        headers: {..._baseHeaders(token: token), 'Prefer': 'resolution=merge-duplicates'},
        body: jsonEncode({
          'user_id': userId, 'item_id': p.itemId, 'title': p.title,
          'image_url': p.imageUrl, 'episode_id': p.episodeId,
          'episode_title': p.episodeTitle,
          'progress_seconds': p.progressSeconds, 'duration_seconds': p.durationSeconds,
          'video_url': p.videoUrl, 'video_url_720': p.videoUrl720,
          'video_url_1080': p.videoUrl1080, 'video_url_360': p.videoUrl360,
          'video_url_4k': p.videoUrl4k,
          'subtitle_url': p.subtitleUrl, 'subtitle_vtt_url': p.subtitleVttUrl,
          'is_movie': p.isMovie,
          'updated_at': p.updatedAt.toIso8601String(),
        }),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  Future<bool> deleteProgress(String itemId) async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final resp = await http.delete(
        Uri.parse('$_supabaseUrl/rest/v1/user_progress?user_id=eq.$userId&item_id=eq.$itemId'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  // -- Feedback -----------------------------------------------------------
  Future<bool> submitFeedback({required String type, required String message}) async {
    final token = AuthSession.instance.accessToken;
    final user = AuthSession.instance.user;
    if (token == null || user == null) return false;
    try {
      final resp = await http.post(
        Uri.parse('$_supabaseUrl/rest/v1/feedback'),
        headers: {..._baseHeaders(token: token), 'Prefer': 'return=representation'},
        body: jsonEncode({
          'user_id': user.id, 'display_name': user.displayName,
          'email': user.email ?? '', 'type': type, 'message': message,
        }),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  Future<List<FeedbackItem>> fetchMyFeedback() async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return [];
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/rest/v1/feedback?user_id=eq.$userId&select=*&order=created_at.desc'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) {
        final rows = jsonDecode(resp.body) as List<dynamic>;
        return rows.map((r) => FeedbackItem.fromJson(r as Map<String, dynamic>)).toList();
      }
    } catch (_) {}
    return [];
  }

  Future<List<FeedbackItem>> fetchAllFeedback() async {
    final token = AuthSession.instance.accessToken;
    if (token == null) return [];
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/rest/v1/feedback?select=*&order=created_at.desc'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) {
        final rows = jsonDecode(resp.body) as List<dynamic>;
        return rows.map((r) => FeedbackItem.fromJson(r as Map<String, dynamic>)).toList();
      }
    } catch (_) {}
    return [];
  }

  Future<bool> updateFeedbackStatus(String id, String status) async {
    final token = AuthSession.instance.accessToken;
    if (token == null) return false;
    try {
      final resp = await http.patch(
        Uri.parse('$_supabaseUrl/rest/v1/feedback?id=eq.$id'),
        headers: _baseHeaders(token: token),
        body: jsonEncode({'status': status}),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  // -- Watchlists ---------------------------------------------------------
  Future<List<Map<String, dynamic>>> fetchWatchlists() async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return [];
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/rest/v1/user_watchlists?user_id=eq.$userId&select=*&order=created_at.desc'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) return List<Map<String, dynamic>>.from(jsonDecode(resp.body) as List);
    } catch (_) {}
    return [];
  }

  Future<List<Map<String, dynamic>>> fetchWatchlistItems(String listId) async {
    final token = AuthSession.instance.accessToken;
    if (token == null) return [];
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/rest/v1/user_watchlist_items?list_id=eq.$listId&select=*&order=added_at.desc'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) return List<Map<String, dynamic>>.from(jsonDecode(resp.body) as List);
    } catch (_) {}
    return [];
  }

  Future<bool> upsertWatchlist(String id, String name, bool isPrivate) async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final resp = await http.post(
        Uri.parse('$_supabaseUrl/rest/v1/user_watchlists'),
        headers: {..._baseHeaders(token: token), 'Prefer': 'resolution=merge-duplicates'},
        body: jsonEncode({
          'id': id, 'user_id': userId, 'name': name,
          'is_private': isPrivate, 'updated_at': DateTime.now().toIso8601String(),
        }),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  Future<bool> deleteWatchlistRemote(String listId) async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final resp = await http.delete(
        Uri.parse('$_supabaseUrl/rest/v1/user_watchlists?id=eq.$listId&user_id=eq.$userId'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  Future<bool> upsertWatchlistItem(String listId, Map<String, dynamic> item) async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final resp = await http.post(
        Uri.parse('$_supabaseUrl/rest/v1/user_watchlist_items'),
        headers: {..._baseHeaders(token: token), 'Prefer': 'resolution=merge-duplicates'},
        body: jsonEncode({...item, 'list_id': listId, 'user_id': userId}),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  Future<bool> deleteWatchlistItem(String listId, String itemId) async {
    final token = AuthSession.instance.accessToken;
    if (token == null) return false;
    try {
      final resp = await http.delete(
        Uri.parse('$_supabaseUrl/rest/v1/user_watchlist_items?list_id=eq.$listId&item_id=eq.$itemId'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  // -- Profile ------------------------------------------------------------
  Future<Map<String, dynamic>?> fetchProfile() async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return null;
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/rest/v1/profiles?id=eq.$userId&select=*'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) {
        final rows = jsonDecode(resp.body) as List<dynamic>;
        if (rows.isNotEmpty) return rows.first as Map<String, dynamic>;
      }
    } catch (_) {}
    return null;
  }

  Future<bool> updateProfile({String? displayName, String? avatarUrl}) async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final body = <String, dynamic>{};
      if (displayName != null) body['display_name'] = displayName;
      if (avatarUrl != null) body['avatar_url'] = avatarUrl;
      if (body.isEmpty) return true;
      // Update profiles table
      final resp = await http.patch(
        Uri.parse('$_supabaseUrl/rest/v1/profiles?id=eq.$userId'),
        headers: {..._baseHeaders(token: token), 'Prefer': 'return=representation'},
        body: jsonEncode(body),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode >= 200 && resp.statusCode < 300 && displayName != null) {
        // Also update auth user_metadata
        await http.put(
          Uri.parse('$_supabaseUrl/auth/v1/user'),
          headers: _baseHeaders(token: token),
          body: jsonEncode({'data': {'display_name': displayName}}),
        ).timeout(const Duration(seconds: 15));
        AuthSession.instance.user?.updateDisplayName(displayName);
      }
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  Future<String?> uploadAvatar(String userId, List<int> bytes, String ext) async {
    final token = AuthSession.instance.accessToken;
    if (token == null) return null;
    try {
      final path = '$userId/avatar.$ext';
      final mime = ext == 'jpg' ? 'image/jpeg' : 'image/$ext';
      final bodyBytes = Uint8List.fromList(bytes);
      final resp = await http.put(
        Uri.parse('$_supabaseUrl/storage/v1/object/avatars/$path'),
        headers: {
          'Authorization': 'Bearer $token',
          'apikey': _anonKey,
          'Content-Type': mime,
          'Content-Length': '${bodyBytes.length}',
          'x-upsert': 'true',
          'cache-control': '3600',
        },
        body: bodyBytes,
      ).timeout(const Duration(seconds: 60));
      if (resp.statusCode >= 200 && resp.statusCode < 300) {
        return '$_supabaseUrl/storage/v1/object/public/avatars/$path?t=${DateTime.now().millisecondsSinceEpoch}';
      }
      // Log error for debugging
      debugPrint('Avatar upload failed: ${resp.statusCode} ${resp.body}');
    } catch (e) {
      debugPrint('Avatar upload exception: $e');
    }
    return null;
  }

  // -- Admin check --------------------------------------------------------
  Future<bool> fetchIsAdmin() async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/rest/v1/profiles?id=eq.$userId&select=is_admin'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) {
        final rows = jsonDecode(resp.body) as List<dynamic>;
        if (rows.isNotEmpty) return rows.first['is_admin'] as bool? ?? false;
      }
    } catch (_) {}
    return false;
  }

  // -- Comments -----------------------------------------------------------
  Future<List<CommentItem>> fetchComments(String itemId) async {
    final token = AuthSession.instance.accessToken;
    if (token == null) return [];
    try {
      final resp = await http.get(
        Uri.parse('$_supabaseUrl/rest/v1/comments?item_id=eq.$itemId&select=*&order=created_at.desc'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      if (resp.statusCode == 200) {
        final rows = jsonDecode(resp.body) as List<dynamic>;
        return rows.map((r) => CommentItem.fromJson(r as Map<String, dynamic>)).toList();
      }
    } catch (_) {}
    return [];
  }

  Future<bool> postComment(String itemId, String text) async {
    final token = AuthSession.instance.accessToken;
    final user = AuthSession.instance.user;
    if (token == null || user == null) return false;
    try {
      final resp = await http.post(
        Uri.parse('$_supabaseUrl/rest/v1/comments'),
        headers: {..._baseHeaders(token: token), 'Prefer': 'return=representation'},
        body: jsonEncode({
          'item_id': itemId, 'user_id': user.id,
          'display_name': user.displayName, 'text': text,
        }),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }

  Future<bool> deleteComment(String commentId) async {
    final token = AuthSession.instance.accessToken;
    final userId = AuthSession.instance.user?.id;
    if (token == null || userId == null) return false;
    try {
      final resp = await http.delete(
        Uri.parse('$_supabaseUrl/rest/v1/comments?id=eq.$commentId&user_id=eq.$userId'),
        headers: _baseHeaders(token: token),
      ).timeout(const Duration(seconds: 15));
      return resp.statusCode >= 200 && resp.statusCode < 300;
    } catch (_) { return false; }
  }
}
""")

print("✅ supabase_manager.dart written")

# --- lib/providers/watch_progress_store.dart --------------------------------
w("lib/providers/watch_progress_store.dart", r"""import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/watch_progress.dart';
import '../services/auth_session.dart';
import '../services/supabase_manager.dart';

class WatchProgressStore extends ChangeNotifier {
  static final WatchProgressStore instance = WatchProgressStore._();
  WatchProgressStore._();

  static const _key = 'UTanWatchProgress_v4';

  final Map<String, WatchProgress> _all = {};
  final Map<String, Timer> _debounceTimers = {};

  Map<String, WatchProgress> get all => Map.unmodifiable(_all);

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(_key);
    if (data != null) {
      try {
        final map = jsonDecode(data) as Map<String, dynamic>;
        for (final e in map.entries) {
          _all[e.key] = WatchProgress.fromJson(e.value as Map<String, dynamic>);
        }
      } catch (_) {}
    }
    notifyListeners();
  }

  void save({
    required String itemId, required String title, required String imageUrl,
    required String episodeId, required String episodeTitle,
    required double progress, required double duration,
    required String videoUrl, required String videoUrl720,
    required String videoUrl1080, required String videoUrl360,
    required String videoUrl4k, required String subUrl,
    required String subVttUrl, bool isMovie = true,
  }) {
    final record = WatchProgress(
      itemId: itemId, title: title, imageUrl: imageUrl,
      episodeId: episodeId, episodeTitle: episodeTitle,
      progressSeconds: progress, durationSeconds: duration,
      updatedAt: DateTime.now(),
      videoUrl: videoUrl, videoUrl720: videoUrl720, videoUrl1080: videoUrl1080,
      videoUrl360: videoUrl360, videoUrl4k: videoUrl4k,
      subtitleUrl: subUrl, subtitleVttUrl: subVttUrl, isMovie: isMovie,
    );
    final pKey = WatchProgress.progressKey(itemId, episodeId);
    _all[pKey] = record;
    _persist();
    notifyListeners();

    if (!AuthSession.instance.isLoggedIn) return;
    _debounceTimers[pKey]?.cancel();
    _debounceTimers[pKey] = Timer(const Duration(seconds: 3), () {
      _debounceTimers.remove(pKey);
      SupabaseManager.instance.upsertProgress(record);
    });
  }

  void remove(String itemId) {
    final keys = _all.keys.where((k) => k == itemId || k.startsWith('${itemId}__')).toList();
    for (final k in keys) _all.remove(k);
    _persist();
    notifyListeners();
    if (AuthSession.instance.isLoggedIn) {
      SupabaseManager.instance.deleteProgress(itemId);
    }
  }

  void clearAll() { _all.clear(); _persist(); notifyListeners(); }

  void mergeFromCloud(List<WatchProgress> remote) {
    for (final r in remote) {
      final pKey = WatchProgress.progressKey(r.itemId, r.episodeId);
      final local = _all[pKey];
      if (local == null || r.updatedAt.isAfter(local.updatedAt)) {
        _all[pKey] = r;
      }
    }
    _persist();
    notifyListeners();
  }

  WatchProgress? progressFor(String itemId, {String episodeId = ''}) {
    final pKey = WatchProgress.progressKey(itemId, episodeId);
    return _all[pKey];
  }

  WatchProgress? latestFor(String itemId) {
    final matches = _all.values.where((p) => p.itemId == itemId).toList()
      ..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
    return matches.firstOrNull;
  }

    List<WatchProgress> get recent {
    final latest = <String, WatchProgress>{};
    for (final p in _all.values) {
      final ex = latest[p.itemId];
      if (ex == null || p.updatedAt.isAfter(ex.updatedAt)) latest[p.itemId] = p;
    }
    return latest.values.toList()..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
  }

  List<WatchProgress> get allEpisodes =>
      _all.values.toList()..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    final map = {for (final e in _all.entries) e.key: e.value.toJson()};
    await prefs.setString(_key, jsonEncode(map));
  }
}
""")

# --- lib/providers/favorites_store.dart -------------------------------------
w("lib/providers/favorites_store.dart", r"""import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/video_item.dart';
import '../services/auth_session.dart';
import '../services/supabase_manager.dart';

class FavoritesStore extends ChangeNotifier {
  static final FavoritesStore instance = FavoritesStore._();
  FavoritesStore._();

  static const _key = 'UTanFavorites_v1';
  final List<VideoItem> _items = [];

  List<VideoItem> get items => List.unmodifiable(_items);

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(_key);
    if (data != null) {
      try {
        final list = jsonDecode(data) as List<dynamic>;
        _items.addAll(list.map((e) => VideoItem.fromJson(e as Map<String, dynamic>)));
      } catch (_) {}
    }
    notifyListeners();
  }

  bool isFavorite(String id) => _items.any((i) => i.id == id);

  void toggle(VideoItem item) {
    final wasPresent = _items.any((i) => i.id == item.id);
    if (wasPresent) {
      _items.removeWhere((i) => i.id == item.id);
    } else {
      _items.insert(0, item);
    }
    _persist();
    notifyListeners();

    if (!AuthSession.instance.isLoggedIn) return;
    if (wasPresent) {
      SupabaseManager.instance.deleteFavorite(item.id).then((ok) {
        if (!ok) { _items.insert(0, item); _persist(); notifyListeners(); }
      });
    } else {
      SupabaseManager.instance.upsertFavorite(item).then((ok) {
        if (!ok) { _items.removeWhere((i) => i.id == item.id); _persist(); notifyListeners(); }
      });
    }
  }

  void mergeFromCloud(List<VideoItem> remote) {
    final localIds = _items.map((i) => i.id).toSet();
    for (final item in remote) {
      if (!localIds.contains(item.id)) _items.add(item);
    }
    _persist();
    notifyListeners();
  }

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, jsonEncode(_items.map((i) => i.toJson()).toList()));
  }
}
""")

# --- lib/providers/watchlist_store.dart -------------------------------------
w("lib/providers/watchlist_store.dart", r"""import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/watch_list.dart';
import '../models/video_item.dart';
import '../services/auth_session.dart';
import '../services/supabase_manager.dart';

class WatchlistStore extends ChangeNotifier {
  static final WatchlistStore instance = WatchlistStore._();
  WatchlistStore._();

  static const _key = 'UTanWatchLists_v1';
  final List<WatchList> _lists = [];

  List<WatchList> get lists => List.unmodifiable(_lists);

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(_key);
    if (data != null) {
      try {
        final list = jsonDecode(data) as List<dynamic>;
        _lists.addAll(list.map((e) => WatchList.fromJson(e as Map<String, dynamic>)));
      } catch (_) {}
    }
    notifyListeners();
    // Sync cloud if logged in
    if (AuthSession.instance.isLoggedIn) unawaited(fetchFromCloud());
  }

  // -- Cloud sync -------------------------------------------------
  Future<void> fetchFromCloud() async {
    try {
      final sm = SupabaseManager.instance;
      final rawLists = await sm.fetchWatchlists();
      final cloudLists = <WatchList>[];
      for (final r in rawLists) {
        final rawItems = await sm.fetchWatchlistItems(r['id'] as String);
        final items = rawItems.map((i) => WatchListItem(
          id: i['item_id'] as String,
          title: i['title'] as String? ?? '',
          imageUrl: i['image_url'] as String? ?? '',
          type: i['type'] as String? ?? 'post',
          addedAt: DateTime.tryParse(i['added_at'] as String? ?? '') ?? DateTime.now(),
        )).toList();
        cloudLists.add(WatchList(
          id: r['id'] as String,
          name: r['name'] as String,
          isPrivate: r['is_private'] as bool? ?? true,
          items: items,
          createdAt: DateTime.tryParse(r['created_at'] as String? ?? '') ?? DateTime.now(),
        ));
      }
      // Merge: cloud wins on conflict (same id)
      for (final cl in cloudLists) {
        final idx = _lists.indexWhere((l) => l.id == cl.id);
        if (idx == -1) { _lists.add(cl); } else { _lists[idx] = cl; }
      }
      await _persist(); notifyListeners();
    } catch (_) {}
  }

  Future<void> _syncListToCloud(WatchList list) async {
    if (!AuthSession.instance.isLoggedIn) return;
    try {
      final sm = SupabaseManager.instance;
      await sm.upsertWatchlist(list.id, list.name, list.isPrivate);
      for (final item in list.items) {
        await sm.upsertWatchlistItem(list.id, {
          'item_id': item.id, 'title': item.title,
          'image_url': item.imageUrl, 'type': item.type,
          'added_at': item.addedAt.toIso8601String(),
        });
      }
    } catch (_) {}
  }

  // -- Local + cloud mutations -------------------------------------
  void createList(String name, {bool isPrivate = true}) {
    final list = WatchList(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: name, isPrivate: isPrivate,
    );
    _lists.insert(0, list);
    _persist(); notifyListeners();
    unawaited(_syncListToCloud(list));
  }

  void deleteList(String id) {
    _lists.removeWhere((l) => l.id == id);
    _persist(); notifyListeners();
    if (AuthSession.instance.isLoggedIn) {
      unawaited(SupabaseManager.instance.deleteWatchlistRemote(id));
    }
  }

  void renameList(String id, String name) {
    final idx = _lists.indexWhere((l) => l.id == id);
    if (idx == -1) return;
    _lists[idx] = WatchList(
      id: _lists[idx].id, name: name,
      isPrivate: _lists[idx].isPrivate,
      items: _lists[idx].items,
      createdAt: _lists[idx].createdAt,
    );
    _persist(); notifyListeners();
    unawaited(SupabaseManager.instance.upsertWatchlist(id, name, _lists[idx].isPrivate));
  }

  void addItem(VideoItem item, String listId) {
    final idx = _lists.indexWhere((l) => l.id == listId);
    if (idx == -1) return;
    if (_lists[idx].items.any((i) => i.id == item.id)) return;
    final wItem = WatchListItem.fromVideo(item);
    _lists[idx].items.insert(0, wItem);
    _persist(); notifyListeners();
    if (AuthSession.instance.isLoggedIn) {
      unawaited(SupabaseManager.instance.upsertWatchlistItem(listId, {
        'item_id': wItem.id, 'title': wItem.title,
        'image_url': wItem.imageUrl, 'type': wItem.type,
        'added_at': wItem.addedAt.toIso8601String(),
      }));
    }
  }

  void removeItem(String itemId, String listId) {
    final idx = _lists.indexWhere((l) => l.id == listId);
    if (idx == -1) return;
    _lists[idx].items.removeWhere((i) => i.id == itemId);
    _persist(); notifyListeners();
    if (AuthSession.instance.isLoggedIn) {
      unawaited(SupabaseManager.instance.deleteWatchlistItem(listId, itemId));
    }
  }

  bool isInAnyList(String itemId) =>
      _lists.any((l) => l.items.any((i) => i.id == itemId));

  List<WatchList> listsContaining(String itemId) =>
      _lists.where((l) => l.items.any((i) => i.id == itemId)).toList();

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, jsonEncode(_lists.map((l) => l.toJson()).toList()));
  }
}

// Helper to fire-and-forget without lint warning
void unawaited(Future<void> f) => f.ignore();
""")

print("✅ Providers written")

# --- lib/providers/download_store.dart ---------------------------------------
w("lib/providers/download_store.dart", r"""import 'dart:async';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:path_provider/path_provider.dart';
import 'package:dio/dio.dart';
import 'dart:convert';
import '../models/download_item.dart';
import '../app_settings.dart';

const String _userAgent =
    'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36';
const String _referer = 'https://movie.vodu.me/';

class DownloadStore extends ChangeNotifier {
  static final DownloadStore instance = DownloadStore._();
  DownloadStore._();

  static const _key = 'EraDownloads_v1';
  final List<DownloadItem> _items = [];
  final Map<String, CancelToken> _tokens = {};

  List<DownloadItem> get items => List.unmodifiable(_items);
  List<DownloadItem> get completed =>
      _items.where((i) => i.status == DownloadStatus.completed).toList();
  List<DownloadItem> get active =>
      _items.where((i) => i.status == DownloadStatus.downloading ||
          i.status == DownloadStatus.queued).toList();

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(_key);
    if (data != null) {
      try {
        final list = jsonDecode(data) as List<dynamic>;
        _items.addAll(list.map((e) => DownloadItem.fromJson(e as Map<String, dynamic>)));
        // Mark interrupted downloads as failed
        for (final item in _items) {
          if (item.status == DownloadStatus.downloading ||
              item.status == DownloadStatus.queued) {
            item.status = DownloadStatus.failed;
          }
        }
      } catch (_) {}
    }
    notifyListeners();
  }

  DownloadItem? get(String id) =>
      _items.where((i) => i.id == id).firstOrNull;

  bool hasDownload(String id) =>
      _items.any((i) => i.id == id &&
          (i.status == DownloadStatus.completed ||
           i.status == DownloadStatus.downloading));

  Future<String> _downloadsDir() async {
    final custom = AppSettings.instance.downloadPath;
    if (custom.isNotEmpty) {
      final dir = Directory(custom);
      if (!await dir.exists()) await dir.create(recursive: true);
      return custom;
    }
    // Android: use public Downloads/UTan so files are visible in Files app
    if (Platform.isAndroid) {
      final dir = Directory('/storage/emulated/0/Download/UTan');
      try {
        if (!await dir.exists()) await dir.create(recursive: true);
        return dir.path;
      } catch (_) {}
    }
    final base = await getApplicationDocumentsDirectory();
    final dir = Directory('${base.path}/downloads');
    if (!await dir.exists()) await dir.create(recursive: true);
    return dir.path;
  }

  String get currentDownloadsDir {
    final custom = AppSettings.instance.downloadPath;
    if (custom.isNotEmpty) return custom;
    if (Platform.isAndroid) return '/storage/emulated/0/Download/UTan';
    return '';
  }

  Future<void> startDownload(DownloadItem item) async {
    // Remove old failed/cancelled entry with same id
    _items.removeWhere((i) => i.id == item.id &&
        (i.status == DownloadStatus.failed ||
         i.status == DownloadStatus.cancelled));
    if (_items.any((i) => i.id == item.id)) return; // already exists

    _items.insert(0, item);
    notifyListeners();
    await _persist();
    _download(item);
  }

  Future<void> _download(DownloadItem item) async {
    try {
      final dir   = await _downloadsDir();
      final ext   = item.url.contains('.mkv') ? 'mkv' : 'mp4';
      final fname = '${item.id.replaceAll(RegExp(r'[^a-zA-Z0-9_]'), '_')}.$ext';
      final path  = '$dir/$fname';

      item.status   = DownloadStatus.downloading;
      item.filePath = path;
      notifyListeners();

      final cancel = CancelToken();
      _tokens[item.id] = cancel;

      await Dio().download(
        item.url, path,
        options: Options(headers: {
          'User-Agent': _userAgent,
          'Referer': _referer,
        }),
        cancelToken: cancel,
        onReceiveProgress: (received, total) {
          item.downloadedBytes = received;
          item.totalBytes      = total;
          item.progress        = total > 0 ? received / total : 0;
          notifyListeners();
        },
      );

      item.status   = DownloadStatus.completed;
      item.progress = 1.0;
      _tokens.remove(item.id);
      notifyListeners();
      await _persist();
    } on DioException catch (e) {
      if (e.type == DioExceptionType.cancel) {
        item.status = DownloadStatus.cancelled;
      } else {
        item.status = DownloadStatus.failed;
      }
      _tokens.remove(item.id);
      notifyListeners();
      await _persist();
    } catch (_) {
      item.status = DownloadStatus.failed;
      _tokens.remove(item.id);
      notifyListeners();
      await _persist();
    }
  }

  void cancelDownload(String id) {
    _tokens[id]?.cancel();
    _tokens.remove(id);
    final item = get(id);
    if (item != null) {
      item.status = DownloadStatus.cancelled;
      notifyListeners();
      _persist();
    }
  }

  Future<void> deleteDownload(String id) async {
    final item = get(id);
    if (item != null && item.filePath.isNotEmpty) {
      final f = File(item.filePath);
      if (await f.exists()) await f.delete();
    }
    _items.removeWhere((i) => i.id == id);
    notifyListeners();
    await _persist();
  }

  Future<void> retryDownload(String id) async {
    final item = get(id);
    if (item == null) return;
    item.status   = DownloadStatus.queued;
    item.progress = 0;
    notifyListeners();
    await _persist();
    _download(item);
  }

  Future<void> _persist() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, jsonEncode(_items.map((i) => i.toJson()).toList()));
  }
}
""")

# --- lib/widgets/ut_loader.dart ----------------------------------------------
w("lib/widgets/ut_loader.dart", r"""import 'package:flutter/material.dart';
import '../app_colors.dart';

class UTanLoader extends StatelessWidget {
  const UTanLoader({super.key});

  @override Widget build(BuildContext context) {
    return Container(
      color: appBg(),
      child: Center(
        child: Image.asset(
          'assets/images/logo.png',
          width: 130,
          height: 130,
          errorBuilder: (_, __, ___) => Text('Era',
            style: appFontStyle(42, bold: true, color: Colors.white)),
        ),
      ),
    );
  }
}
""")

# --- lib/widgets/poster_card.dart -------------------------------------------
w("lib/widgets/poster_card.dart", r"""import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/video_item.dart';
import '../models/watch_progress.dart';
import '../app_colors.dart';

class PosterCard extends StatelessWidget {
  final VideoItem item;
  final WatchProgress? progress;
  final bool showTitle;
  final double width;
  final double height;

  const PosterCard({
    super.key,
    required this.item,
    this.progress,
    this.showTitle = true,
    this.width = 120,
    this.height = 176,
  });

  @override Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Stack(
          alignment: Alignment.bottomLeft,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: CachedNetworkImage(
                imageUrl: item.imageUrl,
                width: width, height: height, fit: BoxFit.cover,
                placeholder: (_, __) => _shimmer(),
                errorWidget: (_, __, ___) => Container(
                  width: width, height: height,
                  color: const Color(0x1AFFFFFF),
                  child: const Icon(Icons.movie, color: Color(0x33FFFFFF), size: 28),
                ),
              ),
            ),
            if (progress != null && progress!.durationSeconds > 0)
              Positioned(
                left: 8, right: 8, bottom: 8,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(1.5),
                  child: LinearProgressIndicator(
                    value: (progress!.progressSeconds / progress!.durationSeconds).clamp(0, 1),
                    minHeight: 3,
                    backgroundColor: Colors.white24,
                    valueColor: AlwaysStoppedAnimation<Color>(utRed()),
                  ),
                ),
              ),
          ],
        ),
        if (showTitle) ...[
          const SizedBox(height: 6),
          SizedBox(
            width: width,
            child: Text(item.title,
              style: const TextStyle(
                fontSize: 12, fontWeight: FontWeight.w500,
                color: Color(0xE0FFFFFF),
              ),
              maxLines: 2, overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ],
    );
  }

  Widget _shimmer() => Container(
    width: width, height: height,
    decoration: BoxDecoration(
      borderRadius: BorderRadius.circular(10),
      color: const Color(0x17FFFFFF),
    ),
  );
}
""")

# --- lib/widgets/hero_carousel.dart -----------------------------------------
w("lib/widgets/hero_carousel.dart", r"""import 'dart:async';
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:provider/provider.dart';
import '../models/video_item.dart';
import '../providers/favorites_store.dart';
import '../app_colors.dart';
import '../app_settings.dart';

class HeroCarousel extends StatefulWidget {
  final List<VideoItem> items;
  final void Function(String itemId) onTap;

  const HeroCarousel({super.key, required this.items, required this.onTap});
  @override State<HeroCarousel> createState() => _HeroCarouselState();
}

class _HeroCarouselState extends State<HeroCarousel> {
  int _current = 0;
  Timer? _timer;

  @override void initState() {
    super.initState();
    _startTimer();
  }

  void _startTimer() {
    _timer?.cancel();
    final count = _displayCount;
    if (count <= 1) return;
    _timer = Timer.periodic(const Duration(seconds: 6), (_) {
      if (!mounted) return;
      setState(() => _current = (_current + 1) % count);
    });
  }

  void _resetTimer() {
    _timer?.cancel();
    _startTimer();
  }

  int get _displayCount => widget.items.length.clamp(0, 8);

  @override void dispose() { _timer?.cancel(); super.dispose(); }

  @override Widget build(BuildContext context) {
    final items = widget.items.take(8).toList();
    if (items.isEmpty) return const SizedBox(height: 380);
    final item = items[_current.clamp(0, items.length - 1)];
    final h = MediaQuery.of(context).size.height * 0.62;

    return GestureDetector(
      onHorizontalDragEnd: (d) {
        final count = _displayCount;
        if (count <= 1) return;
        if (d.primaryVelocity != null && d.primaryVelocity! < -200) {
          setState(() => _current = (_current + 1) % count);
          _resetTimer();
        } else if (d.primaryVelocity != null && d.primaryVelocity! > 200) {
          setState(() => _current = (_current - 1 + count) % count);
          _resetTimer();
        }
      },
      child: SizedBox(
        height: h,
        child: Stack(
          alignment: Alignment.bottomLeft,
          children: [
            // Full-bleed cinematic image
            AnimatedSwitcher(
              duration: const Duration(milliseconds: 700),
              child: CachedNetworkImage(
                key: ValueKey(item.id),
                imageUrl: item.imageUrl,
                fit: BoxFit.cover,
                width: double.infinity,
                height: h,
                placeholder: (_, __) => Container(color: const Color(0x0AFFFFFF)),
                errorWidget:  (_, __, ___) => Container(color: const Color(0x0AFFFFFF)),
              ),
            ),

            // Top vignette - protect status bar
            Positioned(
              top: 0, left: 0, right: 0,
              child: Container(
                height: 120,
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter, end: Alignment.bottomCenter,
                    colors: [Colors.black.withOpacity(0.55), Colors.transparent],
                  ),
                ),
              ),
            ),

            // Logo top-left
            Positioned(
              top: 0, left: 0, right: 0,
              child: SafeArea(
                bottom: false,
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 6),
                  child: Row(children: [
                    Image.asset(
                      'assets/images/logo.png',
                      height: 36,
                      errorBuilder: (_, __, ___) => Text('Era',
                        style: appFontStyle(22, bold: true, color: Colors.white)),
                    ),
                  ]),
                ),
              ),
            ),

            // Bottom cinematic triple-fade (tinted with theme color)
            Positioned(
              bottom: 0, left: 0, right: 0,
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                Container(height: 80,
                  decoration: BoxDecoration(gradient: LinearGradient(
                    begin: Alignment.topCenter, end: Alignment.bottomCenter,
                    colors: [Colors.transparent, utRed().withOpacity(0.08)],
                  )),
                ),
                Container(height: 120,
                  decoration: BoxDecoration(gradient: LinearGradient(
                    begin: Alignment.topCenter, end: Alignment.bottomCenter,
                    colors: [utRed().withOpacity(0.08), appBg().withOpacity(0.75)],
                  )),
                ),
                Container(height: 100,
                  decoration: BoxDecoration(gradient: LinearGradient(
                    begin: Alignment.topCenter, end: Alignment.bottomCenter,
                    colors: [appBg().withOpacity(0.75), appBg()],
                  )),
                ),
                Container(height: 30, color: appBg()),
              ]),
            ),

            // Centered content
            Positioned(
              bottom: 0, left: 0, right: 0,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 22),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Type pill
                    Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                      Text(
                        item.type == 'series'
                          ? L('مسلسل', 'SERIES') : L('فيلم', 'FILM'),
                        style: const TextStyle(
                          fontSize: 11, fontWeight: FontWeight.w600,
                          color: Colors.white, letterSpacing: 1.5),
                      ),
                      const SizedBox(width: 6),
                      Container(width: 3, height: 3,
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.4), shape: BoxShape.circle)),
                      const SizedBox(width: 6),
                      const Text('HD', style: TextStyle(
                        fontSize: 11, fontWeight: FontWeight.w600,
                        color: Colors.white60, letterSpacing: 1.2)),
                      const SizedBox(width: 6),
                      Container(width: 3, height: 3,
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.4), shape: BoxShape.circle)),
                      const SizedBox(width: 6),
                      Text(L('جديد', 'NEW'), style: TextStyle(
                        fontSize: 11, fontWeight: FontWeight.w700,
                        color: utRed(), letterSpacing: 1.5)),
                    ]),
                    const SizedBox(height: 10),

                    // Large cinematic title
                     Text(item.title,
                       textAlign: TextAlign.center,
                       style: const TextStyle(
                         fontSize: 22, fontWeight: FontWeight.w700,
                         color: Colors.white, height: 1.2,
                         shadows: [Shadow(blurRadius: 6, color: Colors.black54, offset: Offset(0,2))],
                       ),
                    ),
                    const SizedBox(height: 14),

                    // Action buttons - capsule style
                     Consumer<FavoritesStore>(builder: (ctx, favs, _) =>
                       Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                        // Play button
                        GestureDetector(
                          onTap: () => widget.onTap(item.id),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 26, vertical: 12),
                            decoration: BoxDecoration(
                              color: Colors.white, borderRadius: BorderRadius.circular(50)),
                            child: Row(mainAxisSize: MainAxisSize.min, children: [
                              const Icon(Icons.play_arrow_rounded, color: Colors.black, size: 18),
                              const SizedBox(width: 6),
                              Text(L('تشغيل', 'Play'),
                                style: const TextStyle(
                                  fontSize: 15, fontWeight: FontWeight.w600, color: Colors.black)),
                            ]),
                          ),
                        ),
                        const SizedBox(width: 10),
                        // My List button
                        GestureDetector(
                          onTap: () => favs.toggle(item),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.15),
                              borderRadius: BorderRadius.circular(50),
                              border: Border.all(color: Colors.white.withOpacity(0.2), width: 0.5),
                            ),
                            child: Row(mainAxisSize: MainAxisSize.min, children: [
                              Icon(favs.isFavorite(item.id) ? Icons.check : Icons.add,
                                color: Colors.white, size: 16),
                              const SizedBox(width: 6),
                              Text(L('قائمتي', 'My List'),
                                style: const TextStyle(fontSize: 14, color: Colors.white)),
                            ]),
                          ),
                        ),
                        const SizedBox(width: 10),
                        // Details button
                        GestureDetector(
                          onTap: () => widget.onTap(item.id),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.15),
                              borderRadius: BorderRadius.circular(50),
                              border: Border.all(color: Colors.white.withOpacity(0.2), width: 0.5),
                            ),
                            child: Row(mainAxisSize: MainAxisSize.min, children: [
                              const Icon(Icons.info_outline, color: Colors.white, size: 16),
                              const SizedBox(width: 6),
                              Text(L('تفاصيل', 'Details'),
                                style: const TextStyle(fontSize: 14, color: Colors.white)),
                            ]),
                          ),
                        ),
                      ]),
                    ),
                    const SizedBox(height: 12),

                    // Dot indicator - animated capsule
                    if (_displayCount > 1)
                      Row(children: [
                        for (int i = 0; i < _displayCount; i++)
                          AnimatedContainer(
                            duration: const Duration(milliseconds: 350),
                            curve: Curves.easeOutBack,
                            margin: const EdgeInsets.only(right: 4),
                            width:  i == _current ? 18 : 5,
                            height: 3,
                            decoration: BoxDecoration(
                              color: i == _current
                                  ? Colors.white : Colors.white.withOpacity(0.25),
                              borderRadius: BorderRadius.circular(2),
                            ),
                          ),
                      ]),
                    const SizedBox(height: 28),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
""")

# --- lib/widgets/category_row.dart ------------------------------------------
w("lib/widgets/category_row.dart", r"""import 'package:flutter/material.dart';
import '../models/video_item.dart';
import '../models/watch_progress.dart';
import '../app_colors.dart';
import '../app_settings.dart';
import 'poster_card.dart';

class CategoryRow extends StatelessWidget {
  final String title;
  final List<VideoItem> items;
  final int tagId;
  final Map<String, WatchProgress> progressMap;
  final void Function(String itemId) onItemTap;
  final void Function(int tagId, String title)? onSeeAll;

  const CategoryRow({
    super.key,
    required this.title,
    required this.items,
    this.tagId = -1,
    required this.progressMap,
    required this.onItemTap,
    this.onSeeAll,
  });

  @override Widget build(BuildContext context) {
    final lang = AppSettings.instance.appLanguage;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title,
                style: const TextStyle(
                  fontSize: 19, fontWeight: FontWeight.w600, color: Colors.white,
                )),
              if (tagId >= 0 && onSeeAll != null)
                GestureDetector(
                  onTap: () => onSeeAll!(tagId, title),
                  child: Row(children: [
                    Text(L('عرض الكل', 'See All'),
                      style: const TextStyle(fontSize: 13, color: Color(0x73FFFFFF))),
                    const Icon(Icons.chevron_right, size: 16, color: Color(0x73FFFFFF)),
                  ]),
                ),
            ],
          ),
        ),
        const SizedBox(height: 14),
        SizedBox(
          height: 220,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 20),
            itemCount: items.length,
            itemBuilder: (_, i) {
              final item = items[i];
              final prog = progressMap[item.id];
              return GestureDetector(
                onTap: () => onItemTap(item.id),
                child: Container(
                  margin: const EdgeInsets.only(right: 12),
                  child: PosterCard(item: item, progress: prog),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
""")

# --- lib/widgets/continue_watching_row.dart ---------------------------------
w("lib/widgets/continue_watching_row.dart", r"""import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/watch_progress.dart';
import '../app_colors.dart';
import '../app_settings.dart';

class ContinueWatchingRow extends StatelessWidget {
  final List<WatchProgress> items;
  final void Function(WatchProgress p) onTap;
  final void Function(String itemId) onRemove;

  const ContinueWatchingRow({
    super.key, required this.items,
    required this.onTap, required this.onRemove,
  });

  @override Widget build(BuildContext context) {
    if (items.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 14),
          child: Text(L('متابعة المشاهدة', 'Continue Watching'),
            style: const TextStyle(
              fontSize: 19, fontWeight: FontWeight.w600, color: Colors.white,
            )),
        ),
        SizedBox(
          height: 160,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 20),
            itemCount: items.length,
            itemBuilder: (_, i) {
              final p = items[i];
              final pct = p.durationSeconds > 0
                  ? (p.progressSeconds / p.durationSeconds).clamp(0.0, 1.0)
                  : 0.0;
              return GestureDetector(
                onTap: () => onTap(p),
                child: Container(
                  width: 150, margin: const EdgeInsets.only(right: 12),
                  child: Stack(children: [
                    ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: Stack(children: [
                        CachedNetworkImage(
                          imageUrl: p.imageUrl, width: 150, height: 120, fit: BoxFit.cover,
                          placeholder: (_, __) => Container(
                            width: 150, height: 120, color: const Color(0x17FFFFFF)),
                          errorWidget: (_, __, ___) => Container(
                            width: 150, height: 120, color: const Color(0x17FFFFFF),
                            child: const Icon(Icons.movie, color: Colors.white24)),
                        ),
                        Positioned(
                          left: 0, right: 0, bottom: 0,
                          child: LinearProgressIndicator(
                            value: pct, minHeight: 3,
                            backgroundColor: Colors.white24,
                            valueColor: AlwaysStoppedAnimation<Color>(utRed()),
                          ),
                        ),
                      ]),
                    ),
                    // Remove button
                    Positioned(
                      top: 4, right: 4,
                      child: GestureDetector(
                        onTap: () => onRemove(p.itemId),
                        child: Container(
                          padding: const EdgeInsets.all(3),
                          decoration: BoxDecoration(
                            color: Colors.black54,
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.close, size: 14, color: Colors.white),
                        ),
                      ),
                    ),
                    // Title
                    Positioned(
                      left: 0, right: 0, bottom: 0,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const SizedBox(height: 122),
                          Text(p.title,
                            style: const TextStyle(
                              fontSize: 11, color: Colors.white70, fontWeight: FontWeight.w500,
                            ),
                            maxLines: 1, overflow: TextOverflow.ellipsis,
                          ),
                          if (!p.isMovie && p.episodeTitle.isNotEmpty)
                            Text(p.episodeTitle,
                              style: const TextStyle(fontSize: 10, color: Colors.white38),
                              maxLines: 1, overflow: TextOverflow.ellipsis,
                            ),
                        ],
                      ),
                    ),
                  ]),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
""")

print("✅ Widget files written")

# --- lib/player/player_screen.dart ------------------------------------------
w("lib/player/player_screen.dart", r"""import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:video_player/video_player.dart';
import 'package:wakelock_plus/wakelock_plus.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:provider/provider.dart';
import '../models/episode_item.dart';
import '../models/subtitle_cue.dart';
import '../services/subtitle_parser.dart';
import '../providers/watch_progress_store.dart';
import '../app_colors.dart';
import '../app_settings.dart';

enum VideoQuality { auto, q360, q720, q1080, q4k }

class PlayerScreen extends StatefulWidget {
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

  const PlayerScreen({
    super.key,
    required this.itemId, required this.itemTitle, required this.itemImageUrl,
    required this.isMovie,
    required this.videoUrl, this.videoUrl720 = '', this.videoUrl1080 = '',
    this.videoUrl360 = '', this.videoUrl4k = '',
    this.subtitleUrl = '', this.subtitleVttUrl = '',
    required this.episodeId, required this.episodeTitle,
    this.episodes = const [],
  });

  @override State<PlayerScreen> createState() => _PlayerScreenState();
}

class _PlayerScreenState extends State<PlayerScreen> {
  VideoPlayerController? _vpc;
  bool _isPlaying = false;
  bool _showControls = true;
  bool _isBuffering = false;
  bool _isFinished = false;
  bool _isLocked = false;
  bool _showEpisodes = false;
  bool _showSubtitleSettings = false;
  String _selectedDrawerSeason = '';
  bool _isSpeedMode = false;
  String? _errorMessage;

  // Subtitle state
  List<SubtitleCue> _cues = [];
  String _activeSub = '';
  String _activeTopSub = '';
  Timer? _subTimer;

  // Controls hide timer
  Timer? _hideTimer;
  Timer? _saveTimer;
  Timer? _upNextTimer;

  double _currentTime = 0;
  double _duration = 0;
  double _volumeValue = 1.0;
  double _brightnessValue = 1.0;
  bool _showVolumeHud = false;
  bool _showBrightnessHud = false;
  Timer? _hudTimer;

  bool _showUpNext = false;
  int _upNextCountdown = 10;
  EpisodeItem? _nextEpisodeItem;
  String? _autoNextSkippedFor;

  VideoQuality _quality = VideoQuality.auto;
  double _playbackSpeed = 1.0;
  bool _showSpeedMenu = false;
  bool _showQualityMenu = false;

  // Current episode tracking
  String _currentEpisodeId = '';
  String _currentEpisodeTitle = '';

  // Seek feedback
  bool _showSeekFeedback = false;
  bool _seekRight = false;
  Timer? _seekFeedbackTimer;

  @override
  void initState() {
    super.initState();
    _currentEpisodeId = widget.episodeId;
    _currentEpisodeTitle = widget.episodeTitle;
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersive);
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.landscapeLeft, DeviceOrientation.landscapeRight,
    ]);
    WakelockPlus.enable();
    _initQuality();
    _setupPlayer();
    _loadSubtitles();
  }

  void _initQuality() {
    final pref = AppSettings.instance.preferredQuality;
    if (pref == 'q720' && widget.videoUrl720.isNotEmpty) _quality = VideoQuality.q720;
    else if (pref == 'q1080' && widget.videoUrl1080.isNotEmpty) _quality = VideoQuality.q1080;
    else if (pref == 'q360' && widget.videoUrl360.isNotEmpty) _quality = VideoQuality.q360;
    else _quality = VideoQuality.auto;
  }

  String _resolvedUrl({VideoQuality? q}) {
    q ??= _quality;
    String fix(String u) {
      if (u.isEmpty) return '';
      if (u.startsWith('http')) return u;
      return 'https://movie.vodu.me/$u';
    }
    switch (q) {
      case VideoQuality.q360: return fix(widget.videoUrl360.isNotEmpty ? widget.videoUrl360 : widget.videoUrl);
      case VideoQuality.q720: return fix(widget.videoUrl720.isNotEmpty ? widget.videoUrl720 : widget.videoUrl);
      case VideoQuality.q1080: return fix(widget.videoUrl1080.isNotEmpty ? widget.videoUrl1080 : widget.videoUrl);
      case VideoQuality.q4k: return fix(widget.videoUrl4k.isNotEmpty ? widget.videoUrl4k : widget.videoUrl);
      default: return fix(widget.videoUrl);
    }
  }

  Future<void> _setupPlayer() async {
    final url = _resolvedUrl();
    if (url.isEmpty) { setState(() => _errorMessage = 'الرابط غير متاح'); return; }
    setState(() { _errorMessage = null; _isBuffering = true; });
    // Support local file paths (downloads)
    if (url.startsWith('/') || url.startsWith('file://')) {
      final path = url.replaceFirst('file://', '');
      _vpc = VideoPlayerController.file(File(path));
    } else {
      _vpc = VideoPlayerController.networkUrl(Uri.parse(url));
    }
    try {
      await _vpc!.initialize();
      _vpc!.addListener(_onPlayerUpdate);
      final saved = WatchProgressStore.instance.progressFor(widget.itemId, episodeId: _currentEpisodeId);
      if (saved != null && saved.progressSeconds > 5 && saved.progressSeconds < saved.durationSeconds - 10) {
        await _vpc!.seekTo(Duration(milliseconds: (saved.progressSeconds * 1000).round()));
      }
      _vpc!.play();
      setState(() { _isPlaying = true; _duration = _vpc!.value.duration.inMilliseconds / 1000.0; });
      _scheduleHide();
      _startSaveTimer();
    } catch (e) {
      setState(() { _errorMessage = 'تعذر تشغيل الفيديو. تحقق من اتصالك بالإنترنت.'; _isBuffering = false; });
    }
  }

  void _onPlayerUpdate() {
    if (_vpc == null || !mounted) return;
    final v = _vpc!.value;
    setState(() {
      _isBuffering = v.isBuffering;
      _isPlaying = v.isPlaying;
      _currentTime = v.position.inMilliseconds / 1000.0;
      _duration = v.duration.inMilliseconds / 1000.0;
      if (_duration > 0 && _currentTime >= _duration - 0.5 && !_isFinished) {
        _isFinished = true;
        _isPlaying = false;
        _onVideoEnd();
      }
    });
    _updateSubtitle();
  }

  void _updateSubtitle() {
    if (!AppSettings.instance.subtitlesEnabled || _cues.isEmpty) {
      if (_activeSub.isNotEmpty || _activeTopSub.isNotEmpty) {
        setState(() { _activeSub = ''; _activeTopSub = ''; });
      }
      return;
    }
    final delay = AppSettings.instance.subtitleDelay;
    final t = _currentTime - delay;
    final active = _cues.where((c) => t >= c.startTime && t <= c.endTime).toList();
    String bot = '', top = '';
    if (active.length == 1) { bot = active[0].text; }
    else if (active.length >= 2) { top = active[0].text; bot = active[1].text; }
    setState(() { _activeSub = bot; _activeTopSub = top; });
  }

  Future<void> _loadSubtitles() async {
    final url = widget.subtitleVttUrl.isNotEmpty ? widget.subtitleVttUrl : widget.subtitleUrl;
    if (url.isEmpty) return;
    final cues = await SubtitleParser.parse(url);
    if (mounted) setState(() => _cues = cues);
  }

  void _onVideoEnd() {
    if (!widget.isMovie && widget.episodes.isNotEmpty && AppSettings.instance.autoPlayNextEnabled) {
      final next = _findNextEpisode();
      if (next != null && next.id != _autoNextSkippedFor) {
        _nextEpisodeItem = next;
        _upNextCountdown = AppSettings.instance.autoPlayCountdownSeconds;
        setState(() => _showUpNext = true);
        _upNextTimer?.cancel();
        _upNextTimer = Timer.periodic(const Duration(seconds: 1), (t) {
          if (!mounted) { t.cancel(); return; }
          if (_upNextCountdown <= 1) {
            t.cancel();
            setState(() => _showUpNext = false);
            _switchEpisode(next, autoplay: true);
          } else {
            setState(() => _upNextCountdown--);
          }
        });
      }
    }
  }

  EpisodeItem? _findNextEpisode() {
    if (widget.episodes.isEmpty) return null;
    final idx = widget.episodes.indexWhere((e) => e.id == _currentEpisodeId);
    if (idx == -1 || idx + 1 >= widget.episodes.length) return null;
    return widget.episodes[idx + 1];
  }

  Future<void> _switchEpisode(EpisodeItem ep, {bool autoplay = false}) async {
    _saveProgress();
    _vpc?.removeListener(_onPlayerUpdate);
    await _vpc?.dispose();
    _vpc = null;
    _cues = [];
    _activeSub = ''; _activeTopSub = '';
    _isFinished = false; _showUpNext = false;
    _currentEpisodeId = ep.id;
    _currentEpisodeTitle = ep.title;
    setState(() { _showEpisodes = false; _isBuffering = true; });
    final url = ep.url.startsWith('http') ? ep.url : 'https://movie.vodu.me/\${ep.url}';
    _vpc = VideoPlayerController.networkUrl(Uri.parse(url));
    try {
      await _vpc!.initialize();
      _vpc!.addListener(_onPlayerUpdate);
      if (autoplay) _vpc!.play();
      setState(() { _isPlaying = autoplay; _duration = _vpc!.value.duration.inMilliseconds / 1000.0; });
    } catch (e) {
      setState(() { _errorMessage = 'تعذر تشغيل الحلقة.'; _isBuffering = false; });
    }
    final subUrl = ep.subtitleVttUrl.isNotEmpty ? ep.subtitleVttUrl : ep.subtitleUrl;
    if (subUrl.isNotEmpty) {
      SubtitleParser.parse(subUrl).then((cues) { if (mounted) setState(() => _cues = cues); });
    }
  }

  void _scheduleHide() {
    _hideTimer?.cancel();
    _hideTimer = Timer(const Duration(seconds: 4), () {
      if (mounted) setState(() => _showControls = false);
    });
  }

  void _saveProgress() {
    if (_duration <= 0) return;
    WatchProgressStore.instance.save(
      itemId: widget.itemId, title: widget.itemTitle, imageUrl: widget.itemImageUrl,
      episodeId: _currentEpisodeId, episodeTitle: _currentEpisodeTitle,
      progress: _currentTime, duration: _duration,
      videoUrl: widget.videoUrl, videoUrl720: widget.videoUrl720,
      videoUrl1080: widget.videoUrl1080, videoUrl360: widget.videoUrl360,
      videoUrl4k: widget.videoUrl4k,
      subUrl: widget.subtitleUrl, subVttUrl: widget.subtitleVttUrl,
      isMovie: widget.isMovie,
    );
  }

  void _startSaveTimer() {
    _saveTimer?.cancel();
    _saveTimer = Timer.periodic(const Duration(seconds: 10), (_) => _saveProgress());
  }

  @override void dispose() {
    _saveProgress();
    _hideTimer?.cancel(); _saveTimer?.cancel();
    _upNextTimer?.cancel(); _hudTimer?.cancel();
    _seekFeedbackTimer?.cancel();
    _vpc?.removeListener(_onPlayerUpdate);
    _vpc?.dispose();
    WakelockPlus.disable();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
    super.dispose();
  }

  void _togglePlayPause() {
    if (_vpc == null) return;
    if (_isPlaying) { _vpc!.pause(); } else { _vpc!.play(); }
    setState(() => _isPlaying = !_isPlaying);
    _scheduleHide();
  }

  void _seek(double seconds) {
    if (_vpc == null) return;
    final target = (_currentTime + seconds).clamp(0, _duration);
    _vpc!.seekTo(Duration(milliseconds: (target * 1000).round()));
    _scheduleHide();
  }

  void _doubleTapSeek(bool isRight) {
    _seek(isRight ? 10 : -10);
    setState(() { _showSeekFeedback = true; _seekRight = isRight; });
    _seekFeedbackTimer?.cancel();
    _seekFeedbackTimer = Timer(const Duration(milliseconds: 500), () {
      if (mounted) setState(() => _showSeekFeedback = false);
    });
  }

  @override Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Stack(children: [
          // Video
          if (_vpc != null && _vpc!.value.isInitialized)
            Center(child: AspectRatio(
              aspectRatio: _vpc!.value.aspectRatio,
              child: VideoPlayer(_vpc!),
            ))
          else
            const Center(child: SizedBox.shrink()),

          // Gesture detector
          _buildGestureLayer(),

          // Subtitle overlay
          _buildSubtitles(),

          // Buffering indicator
          if (_isBuffering && !_isFinished && _errorMessage == null)
            const Center(child: CircularProgressIndicator(color: Colors.white)),

          // Error message
          if (_errorMessage != null) _buildError(),

          // Finished overlay
          if (_isFinished) _buildFinishedOverlay(),

          // Speed mode indicator
          if (_isSpeedMode) _buildSpeedIndicator(),

          // Seek feedback
          if (_showSeekFeedback) _buildSeekFeedback(),

          // Volume/Brightness HUD
          if (_showVolumeHud || _showBrightnessHud) _buildHUD(),

          // Controls overlay
          if (_showControls && !_showEpisodes && !_isLocked) _buildControls(),

          // Lock button only
          if (_isLocked) _buildLockButton(),

          // Episodes drawer
          if (_showEpisodes) _buildEpisodesDrawer(),

          // Up Next banner
          if (_showUpNext && _nextEpisodeItem != null) _buildUpNextBanner(),

          // Subtitle settings panel
          if (_showSubtitleSettings) _buildSubtitleSettings(),

          // Episode handle - visible only with controls, hidden when subtitle settings open
          if (!widget.isMovie && widget.episodes.isNotEmpty && !_showEpisodes
              && _showControls && !_showSubtitleSettings)
            _buildEpisodeHandle(),
        ]),
      ),
    );
  }

  Widget _buildGestureLayer() {
    return GestureDetector(
      behavior: HitTestBehavior.translucent,
      onTap: () {
        if (_isLocked) return;
        setState(() => _showControls = !_showControls);
        if (_showControls) _scheduleHide();
      },
      onDoubleTapDown: (d) {
        final x = d.localPosition.dx;
        final w = MediaQuery.of(context).size.width;
        _doubleTapSeek(x > w / 2);
      },
      onDoubleTap: () {},
      onLongPressStart: (_) {
        if (_isLocked || _isSpeedMode) return;
        _vpc?.setPlaybackSpeed(2.0);
        setState(() => _isSpeedMode = true);
      },
      onLongPressEnd: (_) {
        if (_isSpeedMode) {
          _vpc?.setPlaybackSpeed(_playbackSpeed);
          setState(() => _isSpeedMode = false);
        }
      },
      onVerticalDragUpdate: (d) {
        if (_isLocked) return;
        final x = d.localPosition.dx;
        final w = MediaQuery.of(context).size.width;
        final delta = -d.delta.dy / 200;
        if (x > w / 2) {
          _volumeValue = (_volumeValue + delta).clamp(0, 1);
          setState(() => _showVolumeHud = true);
        } else {
          _brightnessValue = (_brightnessValue + delta).clamp(0, 1);
          setState(() => _showBrightnessHud = true);
        }
        _hudTimer?.cancel();
        _hudTimer = Timer(const Duration(milliseconds: 900), () {
          if (mounted) setState(() { _showVolumeHud = false; _showBrightnessHud = false; });
        });
      },
      child: Container(color: Colors.transparent,
        width: double.infinity, height: double.infinity),
    );
  }

  Widget _buildSubtitles() {
    final settings = AppSettings.instance;
    if (!settings.subtitlesEnabled && _activeSub.isEmpty && _activeTopSub.isEmpty) {
      return const SizedBox.shrink();
    }
    return Consumer<AppSettings>(builder: (_, s, __) => IgnorePointer(
      child: Stack(children: [
        if (_activeTopSub.isNotEmpty)
          Positioned(
            top: 54, left: 20, right: 20,
            child: Center(child: _SubText(
              text: _activeTopSub,
              fontName: s.subtitleFontName,
              fontSize: s.subtitleFontSize,
              color: colorFromHex(s.subtitleColorHex),
              bgOpacity: s.subtitleBgOpacity,
              showStroke: s.subtitleShowStroke,
              showShadow: s.subtitleShowShadow,
            )),
          ),
        if (_activeSub.isNotEmpty)
          Positioned(
            bottom: s.subtitleBottomPad, left: 20, right: 20,
            child: Center(child: _SubText(
              text: _activeSub,
              fontName: s.subtitleFontName,
              fontSize: s.subtitleFontSize,
              color: colorFromHex(s.subtitleColorHex),
              bgOpacity: s.subtitleBgOpacity,
              showStroke: s.subtitleShowStroke,
              showShadow: s.subtitleShowShadow,
            )),
          ),
      ]),
    ));
  }

  Widget _buildControls() {
    return Positioned.fill(
      child: Column(children: [
        // Top bar
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter, end: Alignment.bottomCenter,
              colors: [Colors.black.withOpacity(0.7), Colors.transparent],
            ),
          ),
          child: Row(children: [
            IconButton(
              icon: const Icon(Icons.arrow_back, color: Colors.white),
              onPressed: () => Navigator.pop(context),
            ),
            Expanded(
              child: Text(
                widget.isMovie ? widget.itemTitle : '$_currentEpisodeTitle - ${widget.itemTitle}',
                style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w600),
                maxLines: 1, overflow: TextOverflow.ellipsis,
              ),
            ),
            IconButton(
              icon: Icon(_isLocked ? Icons.lock : Icons.lock_open, color: Colors.white),
              onPressed: () => setState(() => _isLocked = !_isLocked),
            ),
            IconButton(
              icon: const Icon(Icons.subtitles, color: Colors.white),
              onPressed: () => setState(() => _showSubtitleSettings = !_showSubtitleSettings),
            ),
            if (!widget.isMovie && widget.episodes.isNotEmpty)
              IconButton(
                icon: const Icon(Icons.list, color: Colors.white),
                onPressed: () => setState(() { _showEpisodes = true; _showControls = false; }),
              ),
            PopupMenuButton<VideoQuality>(
              icon: const Icon(Icons.hd, color: Colors.white),
              color: const Color(0xFF1A1A1A),
              onSelected: (q) => _switchQuality(q),
              itemBuilder: (_) => [
                _qualityItem(VideoQuality.auto, 'تلقائي / Auto'),
                if (widget.videoUrl360.isNotEmpty) _qualityItem(VideoQuality.q360, '360p'),
                if (widget.videoUrl720.isNotEmpty) _qualityItem(VideoQuality.q720, '720p'),
                if (widget.videoUrl1080.isNotEmpty) _qualityItem(VideoQuality.q1080, '1080p'),
                if (widget.videoUrl4k.isNotEmpty) _qualityItem(VideoQuality.q4k, '4K'),
              ],
            ),
            PopupMenuButton<double>(
              icon: const Icon(Icons.speed, color: Colors.white),
              color: const Color(0xFF1A1A1A),
              onSelected: (s) { _playbackSpeed = s; _vpc?.setPlaybackSpeed(s); },
              itemBuilder: (_) => [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
                  .map((s) => PopupMenuItem(value: s,
                    child: Text('${s}x', style: TextStyle(
                      color: s == _playbackSpeed ? utRed() : Colors.white))))
                  .toList(),
            ),
          ]),
        ),
        const Spacer(),
        // Center controls
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          _playerBtn(Icons.replay_10, () => _seek(-10)),
          const SizedBox(width: 20),
          _playerBtn(
            _isPlaying ? Icons.pause_circle_filled : Icons.play_circle_filled,
            _togglePlayPause, size: 64,
          ),
          const SizedBox(width: 20),
          _playerBtn(Icons.forward_10, () => _seek(10)),
        ]),
        const Spacer(),
        // Bottom seek bar
        Container(
          padding: const EdgeInsets.fromLTRB(12, 0, 12, 12),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.bottomCenter, end: Alignment.topCenter,
              colors: [Colors.black.withOpacity(0.7), Colors.transparent],
            ),
          ),
          child: Column(children: [
            SliderTheme(
              data: SliderThemeData(
                thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                overlayShape: const RoundSliderOverlayShape(overlayRadius: 12),
                activeTrackColor: utRed(),
                inactiveTrackColor: Colors.white24,
                thumbColor: utRed(),
                overlayColor: utRed().withOpacity(0.2),
                trackHeight: 3,
              ),
              child: Slider(
                value: _duration > 0 ? _currentTime.clamp(0, _duration) : 0,
                min: 0, max: _duration > 0 ? _duration : 1,
                onChanged: (v) {
                  _vpc?.seekTo(Duration(milliseconds: (v * 1000).round()));
                  setState(() => _currentTime = v);
                  _scheduleHide();
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                Text(formatTime(_currentTime),
                  style: const TextStyle(fontSize: 12, color: Colors.white70, fontFamily: 'monospace')),
                Text(formatTime(_duration),
                  style: const TextStyle(fontSize: 12, color: Colors.white70, fontFamily: 'monospace')),
              ]),
            ),
          ]),
        ),
      ]),
    );
  }

  PopupMenuItem<VideoQuality> _qualityItem(VideoQuality q, String label) =>
      PopupMenuItem(value: q, child: Text(label, style: TextStyle(
        color: q == _quality ? utRed() : Colors.white)));

  Widget _playerBtn(IconData icon, VoidCallback onTap, {double size = 44}) =>
      GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.15),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: Colors.white, size: size),
        ),
      );

  Widget _buildLockButton() => Positioned(
    top: 20, right: 12,
    child: IconButton(
      icon: const Icon(Icons.lock, color: Colors.white),
      onPressed: () => setState(() => _isLocked = false),
    ),
  );

  Widget _buildEpisodeHandle() => Positioned(
    bottom: 0, left: 0, right: 0,
    child: GestureDetector(
      onVerticalDragEnd: (d) {
        if ((d.primaryVelocity ?? 0) < -100) setState(() => _showEpisodes = true);
      },
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter, end: Alignment.bottomCenter,
            colors: [Colors.transparent, Colors.black.withOpacity(0.55)],
          ),
        ),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Container(
            width: 46, height: 5,
            decoration: BoxDecoration(
              color: Colors.white54, borderRadius: BorderRadius.circular(3)),
          ),
          const SizedBox(height: 4),
          Row(mainAxisAlignment: MainAxisAlignment.center, children: [
            const Icon(Icons.expand_less, color: Colors.white70, size: 14),
            const SizedBox(width: 4),
            Text(L('اسحب لأعلى للحلقات', 'Swipe up for Episodes'),
              style: const TextStyle(fontSize: 12, color: Colors.white70, fontWeight: FontWeight.w600)),
          ]),
        ]),
      ),
    ),
  );

  Widget _buildEpisodesDrawer() {
    final episodes = widget.episodes;
    final seasons = <String>[];
    for (final ep in episodes) {
      if (ep.season.isNotEmpty && !seasons.contains(ep.season)) seasons.add(ep.season);
    }
    final hasSeason = seasons.length > 1;
    final selSeason = _selectedDrawerSeason.isEmpty
        ? (seasons.isNotEmpty ? seasons.first : '')
        : _selectedDrawerSeason;
    final filtered = hasSeason
        ? episodes.where((e) => e.season == selSeason).toList()
        : episodes;

    return Positioned.fill(
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter, end: Alignment.bottomCenter,
            colors: [Colors.black.withOpacity(0.97), Colors.black.withOpacity(0.9)],
          ),
        ),
        child: SafeArea(child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header row
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 8, 8, 4),
              child: Row(children: [
                Expanded(child: Text(widget.itemTitle,
                  style: const TextStyle(color: Colors.white70, fontSize: 14,
                    fontWeight: FontWeight.w600),
                  maxLines: 1, overflow: TextOverflow.ellipsis)),
                IconButton(
                  icon: const Icon(Icons.close, color: Colors.white70, size: 22),
                  onPressed: () => setState(() => _showEpisodes = false),
                ),
              ]),
            ),

            // Season picker
            if (hasSeason)
              SizedBox(
                height: 38,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: seasons.length,
                  itemBuilder: (_, i) {
                    final s = seasons[i];
                    final active = s == selSeason;
                    return GestureDetector(
                      onTap: () => setState(() => _selectedDrawerSeason = s),
                      child: Container(
                        margin: const EdgeInsets.only(right: 8),
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 7),
                        decoration: BoxDecoration(
                          color: active ? utRed() : Colors.white.withOpacity(0.12),
                          borderRadius: BorderRadius.circular(20)),
                        child: Text(s, style: TextStyle(
                          color: Colors.white,
                          fontWeight: active ? FontWeight.w700 : FontWeight.w400,
                          fontSize: 12)),
                      ),
                    );
                  },
                ),
              ),
            const SizedBox(height: 10),

            // Horizontal episode cards - iOS style
            SizedBox(
              height: 130,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: filtered.length,
                itemBuilder: (_, i) {
                  final ep = filtered[i];
                  final isCurrent = ep.id == _currentEpisodeId;
                  return GestureDetector(
                    onTap: () => _switchEpisode(ep),
                    child: Container(
                      width: 130,
                      margin: const EdgeInsets.only(right: 10),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Stack(children: [
                            ClipRRect(
                              borderRadius: BorderRadius.circular(6),
                              child: ep.imageUrl.isNotEmpty
                                ? CachedNetworkImage(
                                    imageUrl: ep.imageUrl,
                                    width: 130, height: 73, fit: BoxFit.cover,
                                    placeholder: (_, __) => _epThumb(),
                                    errorWidget: (_, __, ___) => _epThumb(),
                                  )
                                : _epThumb(),
                            ),
                            if (isCurrent)
                              ClipRRect(
                                borderRadius: BorderRadius.circular(6),
                                child: Container(
                                  width: 130, height: 73,
                                  color: Colors.black.withOpacity(0.5),
                                  alignment: Alignment.center,
                                  child: const Icon(Icons.play_arrow_rounded,
                                    color: Colors.white, size: 28),
                                ),
                              ),
                            Positioned.fill(child: Container(
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(6),
                                border: Border.all(
                                  color: isCurrent ? utRed() : Colors.transparent,
                                  width: 2)),
                            )),
                          ]),
                          const SizedBox(height: 5),
                          Text(ep.title,
                            style: TextStyle(
                              color: isCurrent
                                ? utRed() : Colors.white.withOpacity(0.85),
                              fontSize: 11, fontWeight: FontWeight.w500),
                            maxLines: 2, overflow: TextOverflow.ellipsis),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        )),
      ),
    );
  }

  Widget _epThumb() => Container(
    width: 130, height: 73,
    decoration: BoxDecoration(
      color: Colors.white.withOpacity(0.08),
      borderRadius: BorderRadius.circular(6)),
    child: const Icon(Icons.movie_outlined, color: Colors.white24, size: 28));

  Widget _buildUpNextBanner() {
    final next = _nextEpisodeItem!;
    return Positioned(
      bottom: 60, left: 14, right: 14,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.black.withOpacity(0.85),
          borderRadius: BorderRadius.circular(16),
        ),
        child: Row(children: [
          Container(
            width: 56, height: 56,
            decoration: BoxDecoration(
              color: Colors.white12, borderRadius: BorderRadius.circular(12)),
            child: Center(child: Text('$_upNextCountdown',
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w700, color: Colors.white))),
          ),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(L('الحلقة التالية', 'Next Episode'),
              style: const TextStyle(fontSize: 11, color: Colors.white60)),
            Text(next.title,
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: Colors.white),
              maxLines: 1, overflow: TextOverflow.ellipsis),
          ])),
          TextButton(
            onPressed: () {
              _upNextTimer?.cancel();
              setState(() => _showUpNext = false);
              _autoNextSkippedFor = _currentEpisodeId;
            },
            child: Text(L('إلغاء', 'Cancel'),
              style: const TextStyle(color: Colors.white70)),
          ),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(backgroundColor: utRed()),
            icon: const Icon(Icons.play_arrow, size: 16),
            label: Text(L('تشغيل', 'Play')),
            onPressed: () {
              _upNextTimer?.cancel();
              setState(() => _showUpNext = false);
              _switchEpisode(next, autoplay: true);
            },
          ),
        ]),
      ),
    );
  }

  Widget _buildError() => Center(child: Container(
    padding: const EdgeInsets.all(24),
    decoration: BoxDecoration(
      color: Colors.black.withOpacity(0.55),
      borderRadius: BorderRadius.circular(14),
    ),
    child: Column(mainAxisSize: MainAxisSize.min, children: [
      Icon(Icons.error_outline, color: utRed(), size: 34),
      const SizedBox(height: 12),
      Text(_errorMessage!, textAlign: TextAlign.center,
        style: const TextStyle(color: Colors.white)),
      const SizedBox(height: 16),
      ElevatedButton.icon(
        style: ElevatedButton.styleFrom(backgroundColor: utRed()),
        icon: const Icon(Icons.refresh), label: const Text('إعادة المحاولة'),
        onPressed: () { setState(() { _errorMessage = null; }); _setupPlayer(); },
      ),
    ]),
  ));

  Widget _buildFinishedOverlay() => Center(child: Container(
    padding: const EdgeInsets.all(24),
    decoration: BoxDecoration(
      color: Colors.black.withOpacity(0.45),
      borderRadius: BorderRadius.circular(20),
    ),
    child: Column(mainAxisSize: MainAxisSize.min, children: [
      IconButton(
        icon: const Icon(Icons.replay_circle_filled, color: Colors.white, size: 64),
        onPressed: () {
          _vpc?.seekTo(Duration.zero); _vpc?.play();
          setState(() { _isFinished = false; _isPlaying = true; });
        },
      ),
      Text(L('إعادة التشغيل', 'Restart'),
        style: const TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w600)),
    ]),
  ));

  Widget _buildSpeedIndicator() => Positioned(
    top: 60, left: 0, right: 0,
    child: Center(child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.75), borderRadius: BorderRadius.circular(20)),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        const Icon(Icons.fast_forward, color: Colors.white, size: 18),
        const SizedBox(width: 6),
        const Text('2× سرعة',
          style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w700)),
      ]),
    )),
  );

  Widget _buildSeekFeedback() => Positioned(
    bottom: 80, left: 0, right: 0,
    child: Center(child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.6), borderRadius: BorderRadius.circular(30)),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        Icon(_seekRight ? Icons.forward_10 : Icons.replay_10, color: Colors.white, size: 40),
        const SizedBox(width: 8),
        Text(_seekRight ? '+10' : '-10',
          style: const TextStyle(color: Colors.white, fontSize: 20)),
      ]),
    )),
  );

  Widget _buildHUD() => Positioned(
    top: 60, left: 0, right: 0,
    child: Center(child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.6), borderRadius: BorderRadius.circular(14)),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        Icon(
          _showVolumeHud
              ? (_volumeValue <= 0.01 ? Icons.volume_off : Icons.volume_up)
              : (_brightnessValue < 0.5 ? Icons.brightness_3 : Icons.brightness_high),
          color: Colors.white,
        ),
        const SizedBox(width: 10),
        SizedBox(
          width: 110,
          child: LinearProgressIndicator(
            value: _showVolumeHud ? _volumeValue : _brightnessValue,
            color: Colors.white, backgroundColor: Colors.white30,
          ),
        ),
      ]),
    )),
  );

  Widget _buildSubtitleSettings() {
    final s = AppSettings.instance;
    return Positioned(
      bottom: 0, left: 0, right: 0,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFF1A1A1A),
          borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: StatefulBuilder(builder: (ctx, setSt) {
          return Column(mainAxisSize: MainAxisSize.min, children: [
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
              Text(L('إعدادات الترجمة', 'Subtitle Settings'),
                style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w700)),
              IconButton(
                icon: const Icon(Icons.close, color: Colors.white),
                onPressed: () => setState(() => _showSubtitleSettings = false),
              ),
            ]),
            SwitchListTile(
              title: Text(L('تفعيل الترجمة', 'Enable Subtitles'),
                style: const TextStyle(color: Colors.white)),
              value: s.subtitlesEnabled,
              activeColor: utRed(),
              onChanged: (v) { s.subtitlesEnabled = v; setSt(() {}); setState(() {}); },
            ),
            _subSlider(L('تأخير (ثانية)', 'Delay (s)'), s.subtitleDelay, -5, 5, (v) {
              s.subtitleDelay = v; setSt(() {}); }),
            _subSlider(L('حجم الخط', 'Font Size'), s.subtitleFontSize, 12, 36, (v) {
              s.subtitleFontSize = v; setSt(() {}); }),
            _subSlider(L('الموضع من الأسفل', 'Position from bottom'), s.subtitleBottomPad, 0, 200, (v) {
              s.subtitleBottomPad = v; setSt(() {}); setState(() {}); }),
            _subSlider(L('شفافية الخلفية', 'BG Opacity'), s.subtitleBgOpacity, 0, 1, (v) {
              s.subtitleBgOpacity = v; setSt(() {}); }),
            const SizedBox(height: 4),
            Row(children: [
              Expanded(child: SwitchListTile(
                dense: true, contentPadding: EdgeInsets.zero,
                title: Text(L('ظل النص', 'Shadow'),
                  style: const TextStyle(color: Colors.white70, fontSize: 12)),
                value: s.subtitleShowShadow, activeColor: utRed(),
                onChanged: (v) { s.subtitleShowShadow = v; setSt(() {}); setState(() {}); },
              )),
              Expanded(child: SwitchListTile(
                dense: true, contentPadding: EdgeInsets.zero,
                title: Text(L('حد النص', 'Stroke'),
                  style: const TextStyle(color: Colors.white70, fontSize: 12)),
                value: s.subtitleShowStroke, activeColor: utRed(),
                onChanged: (v) { s.subtitleShowStroke = v; setSt(() {}); setState(() {}); },
              )),
            ]),
            const SizedBox(height: 8),
            Wrap(spacing: 8, children: [
              '#FFFFFF', '#FFFF00', '#00FFFF', '#FF69B4', '#FF4444', '#44FF44', '#4444FF',
            ].map((hex) => GestureDetector(
              onTap: () { s.subtitleColorHex = hex; setSt(() {}); setState(() {}); },
              child: Container(
                width: 28, height: 28,
                decoration: BoxDecoration(
                  color: colorFromHex(hex),
                  shape: BoxShape.circle,
                  border: s.subtitleColorHex == hex
                      ? Border.all(color: Colors.white, width: 2) : null,
                ),
              ),
            )).toList()),
            const SizedBox(height: 8),
            Row(children: [
              Text(L('الخط:', 'Font:'), style: const TextStyle(color: Colors.white70, fontSize: 13)),
              const SizedBox(width: 8),
              ...['Cairo', 'Rubik', 'IBMPlexArabic', 'ExpoArabic'].map((f) =>
                GestureDetector(
                  onTap: () { s.subtitleFontName = f; setSt(() {}); setState(() {}); },
                  child: Container(
                    margin: const EdgeInsets.only(right: 8),
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: s.subtitleFontName == f ? utRed() : Colors.white12,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(f, style: TextStyle(
                      color: Colors.white, fontSize: 11,
                      fontFamily: f,
                    )),
                  ),
                )),
            ]),
            const SizedBox(height: 8),
          ]);
        }),
      ),
    );
  }

  Widget _subSlider(String label, double val, double min, double max, ValueChanged<double> onChanged) =>
    Row(children: [
      SizedBox(width: 120,
        child: Text(label, style: const TextStyle(color: Colors.white70, fontSize: 12))),
      Expanded(child: Slider(
        value: val.clamp(min, max), min: min, max: max,
        activeColor: utRed(), inactiveColor: Colors.white24,
        onChanged: onChanged,
      )),
      SizedBox(width: 36, child: Text(val.toStringAsFixed(1),
        style: const TextStyle(color: Colors.white70, fontSize: 11))),
    ]);

  Future<void> _switchQuality(VideoQuality q) async {
    if (_vpc == null) return;
    final t = _currentTime;
    _quality = q;
    AppSettings.instance.preferredQuality = q.name;
    final url = _resolvedUrl(q: q);
    if (url.isEmpty) return;
    _vpc?.removeListener(_onPlayerUpdate);
    await _vpc?.dispose();
    _vpc = VideoPlayerController.networkUrl(Uri.parse(url));
    try {
      await _vpc!.initialize();
      _vpc!.addListener(_onPlayerUpdate);
      await _vpc!.seekTo(Duration(milliseconds: (t * 1000).round()));
      if (_isPlaying) _vpc!.play();
      setState(() {});
    } catch (_) {}
  }
}


class _SubText extends StatelessWidget {
  final String text;
  final String fontName;
  final double fontSize;
  final Color color;
  final double bgOpacity;
  final bool showStroke;
  final bool showShadow;
  const _SubText({required this.text, required this.fontName,
    required this.fontSize, required this.color, required this.bgOpacity,
    this.showStroke = true, this.showShadow = true});

  @override Widget build(BuildContext context) {
    final base = subtitleFontStyle(fontName, fontSize, color: color);
    final stroke = base.copyWith(
      foreground: Paint()
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2.5
        ..color = Colors.black,
      color: null,
    );
    final filled = showShadow ? base.copyWith(shadows: [
      const Shadow(blurRadius: 4, color: Colors.black, offset: Offset(1, 1)),
      const Shadow(blurRadius: 8, color: Colors.black, offset: Offset(-1, -1)),
    ]) : base;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(bgOpacity > 0 ? bgOpacity : 0),
        borderRadius: BorderRadius.circular(8),
      ),
      child: showStroke ? Stack(children: [
        Text(text, style: stroke, textAlign: TextAlign.center),
        Text(text, style: filled, textAlign: TextAlign.center),
      ]) : Text(text, style: filled, textAlign: TextAlign.center),
    );
  }
}
""")

print("✅ player_screen.dart written")

# --- lib/screens/home_screen.dart -------------------------------------------
w("lib/screens/home_screen.dart", r"""import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../services/scraper.dart';
import '../providers/watch_progress_store.dart';
import '../models/video_item.dart';
import '../models/site_category.dart';
import '../app_colors.dart';
import '../app_settings.dart';
import '../widgets/hero_carousel.dart';
import '../providers/favorites_store.dart';
import '../widgets/category_row.dart';
import '../widgets/continue_watching_row.dart';
import 'details_screen.dart';
import 'category_list_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _didLoad = false;

  @override void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_didLoad) {
      _didLoad = true;
      context.read<MovieScraper>().fetchHome();
    }
  }

  @override Widget build(BuildContext context) {
    // Transparent status bar so hero goes edge-to-edge
    SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ));

    final scraper       = context.watch<MovieScraper>();
    final progressStore = context.watch<WatchProgressStore>();
    final recentlyWatched = progressStore.recent;
    final progressMap = { for (final p in recentlyWatched) p.itemId: p };
    final settings      = AppSettings.instance;

    return Scaffold(
      backgroundColor: appBg(),
      extendBodyBehindAppBar: true,
      body: scraper.isLoading && scraper.categories.isEmpty
          ? Container(
              color: appBg(),
              child: Center(child: CircularProgressIndicator(
                color: utRed(), strokeWidth: 2.5)))
          : RefreshIndicator(
              onRefresh: scraper.refreshHome,
              color: utRed(),
              child: CustomScrollView(slivers: [
                SliverToBoxAdapter(child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // -- Hero (edge-to-edge, no top bar) ------------------
                    if (scraper.heroItems.isNotEmpty)
                      HeroCarousel(
                        items: scraper.heroItems.take(10).toList(),
                        onTap: (id) => _openDetails(context, id),
                      ),

                    const SizedBox(height: 24),

                    // -- Continue Watching ---------------------------------
                    if (recentlyWatched.isNotEmpty) ...[
                      ContinueWatchingRow(
                        items: recentlyWatched,
                        onTap: (p) => Navigator.push(context, MaterialPageRoute(
                          builder: (_) => DetailsScreen(itemId: p.itemId))),
                        onRemove: (id) => progressStore.remove(id),
                      ),
                      const SizedBox(height: 24),
                    ],

                    // -- Trending Today (numbered) -------------------------
                    if (scraper.heroItems.length >= 5) ...[
                      Padding(
                        padding: const EdgeInsets.fromLTRB(18, 0, 18, 12),
                        child: Row(children: [
                          Container(width: 3, height: 18,
                            decoration: BoxDecoration(color: utRed(),
                              borderRadius: BorderRadius.circular(2))),
                          const SizedBox(width: 8),
                          Text(L('الأكثر مشاهدة اليوم', 'Trending Today'),
                            style: appFontStyle(17, bold: true)),
                        ]),
                      ),
                      SizedBox(
                        height: 185,
                        child: ListView.builder(
                          scrollDirection: Axis.horizontal,
                          padding: const EdgeInsets.symmetric(horizontal: 12),
                          itemCount: scraper.heroItems.take(10).length,
                          itemBuilder: (_, i) {
                            final item = scraper.heroItems[i];
                            return GestureDetector(
                              onTap: () => _openDetails(context, item.id),
                              child: SizedBox(
                                width: 110,
                                child: Stack(
                                  clipBehavior: Clip.none,
                                  children: [
                                    Positioned(
                                      left: 22, top: 0, right: 0, bottom: 20,
                                      child: ClipRRect(
                                        borderRadius: BorderRadius.circular(10),
                                        child: CachedNetworkImage(
                                          imageUrl: item.imageUrl,
                                          fit: BoxFit.cover,
                                          placeholder: (_, __) => Container(color: Colors.white10),
                                          errorWidget: (_, __, ___) => Container(color: Colors.white10),
                                        ),
                                      ),
                                    ),
                                    Positioned(
                                      left: 0, bottom: 0,
                                      child: Text('${i + 1}',
                                        style: TextStyle(
                                          fontSize: 88, fontWeight: FontWeight.w900,
                                          color: Colors.white,
                                          height: 1,
                                          shadows: [
                                            Shadow(blurRadius: 4, color: Colors.black87,
                                              offset: const Offset(2, 2)),
                                          ],
                                          foreground: Paint()
                                            ..style = PaintingStyle.stroke
                                            ..strokeWidth = 3
                                            ..color = Colors.black54,
                                        ),
                                      ),
                                    ),
                                    Positioned(
                                      left: 0, bottom: 0,
                                      child: Text('${i + 1}',
                                        style: const TextStyle(
                                          fontSize: 88, fontWeight: FontWeight.w900,
                                          color: Colors.white, height: 1,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                      ),
                      const SizedBox(height: 28),
                    ],

                    // -- Browse by Genre -----------------------------------
                    if (scraper.categories.isNotEmpty) ...[
                      Padding(
                        padding: const EdgeInsets.fromLTRB(18, 0, 18, 12),
                        child: Row(children: [
                          Container(width: 3, height: 18,
                            decoration: BoxDecoration(color: utRed(),
                              borderRadius: BorderRadius.circular(2))),
                          const SizedBox(width: 8),
                          Text(L('تصفح بالتصنيف', 'Browse by Genre'),
                            style: appFontStyle(17, bold: true)),
                        ]),
                      ),
                      SizedBox(
                        height: 88,
                        child: ListView.builder(
                          scrollDirection: Axis.horizontal,
                          padding: const EdgeInsets.symmetric(horizontal: 12),
                          itemCount: scraper.categories.take(12).length,
                          itemBuilder: (_, i) {
                            final cat = scraper.categories.take(12).toList()[i];
                            final color = _genreColor(i);
                            return GestureDetector(
                              onTap: () => Navigator.push(context, MaterialPageRoute(
                                builder: (_) => CategoryListScreen(
                                  category: SiteCategory(
                                    id: cat.tagId, remoteId: cat.tagId,
                                    isTag: true, nameAr: cat.name, nameEn: cat.name,
                                  ),
                                ),
                              )),
                              child: Container(
                                width: 130,
                                margin: const EdgeInsets.only(right: 10),
                                decoration: BoxDecoration(
                                  color: color,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Stack(children: [
                                  Positioned(
                                    right: -10, bottom: -10,
                                    child: Icon(Icons.play_circle_outline,
                                      size: 70, color: Colors.white.withOpacity(0.12)),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.all(14),
                                    child: Text(cat.name,
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontWeight: FontWeight.w700,
                                        fontSize: 14),
                                      maxLines: 2),
                                  ),
                                ]),
                              ),
                            );
                          },
                        ),
                      ),
                      const SizedBox(height: 28),
                    ],

                    // -- Category rows from scraper ------------------------
                    ...scraper.categories.map((cat) => Padding(
                      padding: const EdgeInsets.only(bottom: 24),
                      child: CategoryRow(
                        title: cat.name,
                        items: cat.items,
                        tagId: cat.tagId,
                        progressMap: progressMap,
                        onItemTap: (id) => _openDetails(context, id),
                        onSeeAll: (tagId, title) => Navigator.push(context, MaterialPageRoute(
                          builder: (_) => CategoryListScreen(
                            category: SiteCategory(
                              id: tagId, remoteId: tagId, isTag: true,
                              nameAr: title, nameEn: title,
                            ),
                          ),
                        )),
                      ),
                    )),
                    const SizedBox(height: 100),
                  ],
                )),
              ]),
            ),
    );
  }

  Color _genreColor(int i) {
    const colors = [
      Color(0xFF6441A5), Color(0xFF0070CC), Color(0xFFE50914),
      Color(0xFF1DB954), Color(0xFFF5A623), Color(0xFFFF6B6B),
      Color(0xFF17A589), Color(0xFF8E44AD), Color(0xFF2980B9),
      Color(0xFFE74C3C), Color(0xFF27AE60), Color(0xFFD35400),
    ];
    return colors[i % colors.length];
  }

  void _openDetails(BuildContext ctx, String id) {
    Navigator.push(ctx, MaterialPageRoute(builder: (_) => DetailsScreen(itemId: id)));
  }
}
""")


# --- lib/screens/browse_screen.dart -----------------------------------------
w("lib/screens/browse_screen.dart", r"""import 'package:flutter/material.dart';
import '../models/site_category.dart';
import '../app_colors.dart';
import '../app_settings.dart';
import 'category_list_screen.dart';

class BrowseScreen extends StatelessWidget {
  const BrowseScreen({super.key});

  @override Widget build(BuildContext context) {
    final lang = AppSettings.instance.appLanguage;
    return Scaffold(
      backgroundColor: appBg(),
      appBar: AppBar(
        backgroundColor: appBg(),
        title: Text(L('تصفح', 'Browse'),
          style: appFontStyle(20, bold: true)),
        elevation: 0,
      ),
      body: GridView.builder(
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2, childAspectRatio: 2.5, crossAxisSpacing: 14, mainAxisSpacing: 14,
        ),
        itemCount: siteCategories.length,
        itemBuilder: (_, i) {
          final cat = siteCategories[i];
          final color = categoryColor(cat.nameEn);
          return GestureDetector(
            onTap: () => Navigator.push(context, MaterialPageRoute(
              builder: (_) => CategoryListScreen(category: cat))),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 120),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [color.withOpacity(0.5), color.withOpacity(0.12)],
                  begin: Alignment.topRight, end: Alignment.bottomLeft,
                ),
                border: Border.all(color: color.withOpacity(0.25)),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Stack(children: [
                Positioned(
                  top: 8, right: 8,
                  child: Icon(categoryIcon(cat.nameEn),
                    size: 36, color: color.withOpacity(0.3)),
                ),
                Positioned(
                  left: 12, bottom: 10,
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(cat.localizedName(lang),
                      style: TextStyle(
                        fontFamily: 'ExpoArabic', fontSize: 14,
                        fontWeight: FontWeight.w700, color: Colors.white,
                      ),
                      maxLines: 2,
                    ),
                    if (lang == 'ar' && cat.nameEn.isNotEmpty)
                      Text(cat.nameEn,
                        style: const TextStyle(fontSize: 10, color: Colors.white54)),
                  ]),
                ),
              ]),
            ),
          );
        },
      ),
    );
  }
}
""")

print("✅ home + browse screens written")

# --- lib/screens/category_list_screen.dart -----------------------------------
w("lib/screens/category_list_screen.dart", r"""import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/site_category.dart';
import '../models/video_item.dart';
import '../services/scraper.dart';
import '../app_colors.dart';
import '../app_settings.dart';
import '../widgets/poster_card.dart';
import 'details_screen.dart';

class CategoryListScreen extends StatefulWidget {
  final SiteCategory category;
  const CategoryListScreen({super.key, required this.category});
  @override State<CategoryListScreen> createState() => _CategoryListScreenState();
}

class _CategoryListScreenState extends State<CategoryListScreen> {
  final List<VideoItem> _items = [];
  bool _loading = false;
  bool _reachedEnd = false;
  int _page = 1;
  String _sort = 'date';
  String _genre = '';
  final ScrollController _scroll = ScrollController();
  static const _genres = ['Action','Adventure','Animation','Comedy','Drama',
    'Fantasy','Horror','Romance','Sci-Fi','Thriller'];

  @override void initState() {
    super.initState();
    _loadMore();
    _scroll.addListener(() {
      if (_scroll.position.pixels >= _scroll.position.maxScrollExtent - 300) _loadMore();
    });
  }

  @override void dispose() { _scroll.dispose(); super.dispose(); }

  Future<void> _loadMore() async {
    if (_loading || _reachedEnd) return;
    setState(() => _loading = true);
    final scraper = context.read<MovieScraper>();
    final newItems = await scraper.fetchCategory(
      widget.category.remoteId, page: _page,
      useTag: widget.category.isTag, sort: _sort,
      genre: _genre.isEmpty ? null : _genre,
    );
    if (!mounted) return;
    final existingIds = _items.map((i) => i.id).toSet();
    final unique = newItems.where((i) => existingIds.add(i.id)).toList();
    setState(() {
      _items.addAll(unique);
      _loading = false;
      if (newItems.isEmpty || unique.isEmpty) { _reachedEnd = true; }
      else { _page++; }
    });
  }

  Future<void> _reset() async {
    setState(() { _items.clear(); _page = 1; _reachedEnd = false; });
    await _loadMore();
  }

  @override Widget build(BuildContext context) {
    final lang = AppSettings.instance.appLanguage;
    final minWidth = AppSettings.instance.posterMinWidth;
    return Scaffold(
      backgroundColor: appBg(),
      appBar: AppBar(
        backgroundColor: appBg(),
        title: Text(widget.category.localizedName(lang),
          style: appFontStyle(18, bold: true)),
        elevation: 0,
      ),
      body: Column(children: [
        // Sort & filter bar
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 8),
          child: Row(children: [
            Expanded(child: SegmentedButton<String>(
              style: SegmentedButton.styleFrom(
                selectedBackgroundColor: utRed(),
                foregroundColor: Colors.white,
                selectedForegroundColor: Colors.white,
              ),
              segments: [
                ButtonSegment(value: 'date', label: Text(L('تاريخ', 'Date'))),
                ButtonSegment(value: 'year', label: Text(L('سنة', 'Year'))),
                ButtonSegment(value: 'views', label: Text(L('مشاهدات', 'Views'))),
                ButtonSegment(value: 'rating', label: Text(L('تقييم', 'Rating'))),
              ],
              selected: {_sort},
              onSelectionChanged: (s) { _sort = s.first; _reset(); },
            )),
            const SizedBox(width: 8),
            PopupMenuButton<String>(
              icon: Icon(Icons.tune,
                color: _genre.isEmpty ? Colors.white70 : utRed()),
              color: const Color(0xFF1A1A1A),
              onSelected: (g) { _genre = g == 'All' ? '' : g; _reset(); },
              itemBuilder: (_) => [
                PopupMenuItem(value: 'All', child: Text(L('الكل', 'All'),
                  style: const TextStyle(color: Colors.white))),
                ..._genres.map((g) => PopupMenuItem(value: g,
                  child: Text(g, style: const TextStyle(color: Colors.white)))),
              ],
            ),
          ]),
        ),
        Expanded(child: RefreshIndicator(
          onRefresh: _reset,
          color: utRed(),
          child: GridView.builder(
            controller: _scroll,
            padding: const EdgeInsets.all(16),
            gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
              maxCrossAxisExtent: minWidth + 40,
              childAspectRatio: 120 / (176 + 44),
              crossAxisSpacing: 14, mainAxisSpacing: 16,
            ),
            itemCount: _items.length + (_loading || _reachedEnd ? 1 : 0),
            itemBuilder: (_, i) {
              if (i >= _items.length) {
                if (_reachedEnd && _items.isNotEmpty) {
                  return Center(child: Text(L('تم تحميل الكل', 'All loaded'),
                    style: const TextStyle(color: Colors.white38, fontSize: 12)));
                }
                return Center(child: CircularProgressIndicator(color: utRed()));
              }
              final item = _items[i];
              return GestureDetector(
                onTap: () => Navigator.push(context, MaterialPageRoute(
                  builder: (_) => DetailsScreen(itemId: item.id))),
                child: PosterCard(item: item),
              );
            },
          ),
        )),
      ]),
    );
  }
}
""")

# --- lib/screens/search_screen.dart -----------------------------------------
w("lib/screens/search_screen.dart", r"""import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/scraper.dart';
import '../models/video_item.dart';
import '../app_colors.dart';
import '../app_settings.dart';
import '../widgets/poster_card.dart';
import 'details_screen.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});
  @override State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final _titleCtrl = TextEditingController();
  final _genreCtrl = TextEditingController();
  final _yearCtrl  = TextEditingController();
  List<VideoItem> _results = [];
  bool _searching = false;
  bool _showFilters = false;
  Timer? _debounce;

  @override void dispose() {
    _titleCtrl.dispose(); _genreCtrl.dispose(); _yearCtrl.dispose();
    _debounce?.cancel(); super.dispose();
  }

  void _performSearch() {
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 400), () async {
      if (_titleCtrl.text.isEmpty && _genreCtrl.text.isEmpty && _yearCtrl.text.isEmpty) {
        setState(() => _results = []); return;
      }
      setState(() => _searching = true);
      final scraper = context.read<MovieScraper>();
      final r = await scraper.advancedSearch(
        title: _titleCtrl.text,
        genre: _genreCtrl.text,
        year: _yearCtrl.text,
      );
      if (mounted) setState(() { _results = r; _searching = false; });
    });
  }

  @override Widget build(BuildContext context) {
    final lang = AppSettings.instance.appLanguage;
    return Scaffold(
      backgroundColor: appBg(),
      appBar: AppBar(
        backgroundColor: appBg(), elevation: 0,
        title: Text(L('بحث', 'Search'), style: appFontStyle(20, bold: true)),
      ),
      body: Column(children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
          child: Container(
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.08),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(children: [
              const Padding(padding: EdgeInsets.symmetric(horizontal: 12),
                child: Icon(Icons.search, color: Colors.grey)),
              Expanded(child: TextField(
                controller: _titleCtrl,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  border: InputBorder.none,
                  hintText: L('بحث...', 'Search...'),
                  hintStyle: const TextStyle(color: Colors.grey),
                ),
                onChanged: (_) => _performSearch(),
              )),
              if (_searching)
                Padding(padding: const EdgeInsets.symmetric(horizontal: 12),
                  child: SizedBox(width: 18, height: 18,
                    child: CircularProgressIndicator(strokeWidth: 2, color: utRed()))),
              if (_titleCtrl.text.isNotEmpty && !_searching)
                IconButton(
                  icon: const Icon(Icons.close, color: Colors.white54, size: 18),
                  onPressed: () { _titleCtrl.clear(); setState(() => _results = []); },
                ),
              IconButton(
                icon: Icon(Icons.tune, color: _showFilters ? utRed() : Colors.white54),
                onPressed: () => setState(() => _showFilters = !_showFilters),
              ),
            ]),
          ),
        ),

        // Advanced filters
        if (_showFilters)
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
            child: Row(children: [
              Expanded(child: _filterField(_genreCtrl, L('النوع', 'Genre'))),
              const SizedBox(width: 8),
              Expanded(child: _filterField(_yearCtrl, L('السنة', 'Year'))),
              const SizedBox(width: 8),
              ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: utRed()),
                onPressed: _performSearch,
                child: Text(L('بحث', 'Search')),
              ),
            ]),
          ),

        // Results grid
        Expanded(child: _results.isEmpty && !_searching
            ? Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
                Icon(Icons.search, size: 60, color: Colors.white12),
                const SizedBox(height: 16),
                Text(L('ابحث عن أفلامك المفضلة', 'Search your favourite titles'),
                  style: const TextStyle(color: Colors.white38)),
              ]))
            : GridView.builder(
                padding: const EdgeInsets.all(16),
                gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                  maxCrossAxisExtent: 150,
                  childAspectRatio: 120 / 220,
                  crossAxisSpacing: 14, mainAxisSpacing: 16,
                ),
                itemCount: _results.length,
                itemBuilder: (_, i) {
                  final item = _results[i];
                  return GestureDetector(
                    onTap: () => Navigator.push(context, MaterialPageRoute(
                      builder: (_) => DetailsScreen(itemId: item.id))),
                    child: PosterCard(item: item),
                  );
                },
              )),
      ]),
    );
  }

  Widget _filterField(TextEditingController ctrl, String hint) =>
    TextField(
      controller: ctrl,
      style: const TextStyle(color: Colors.white, fontSize: 13),
      decoration: InputDecoration(
        hintText: hint, hintStyle: const TextStyle(color: Colors.grey, fontSize: 13),
        filled: true, fillColor: Colors.white.withOpacity(0.07),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8),
          borderSide: BorderSide.none),
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      ),
    );
}
""")

print("✅ category_list + search screens written")

# --- lib/screens/details_screen.dart ----------------------------------------
w("lib/screens/details_screen.dart", r"""import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:provider/provider.dart';
import '../services/scraper.dart';
import '../models/media_details.dart';
import '../models/video_item.dart';
import '../models/episode_item.dart';
import '../providers/watch_progress_store.dart';
import '../providers/favorites_store.dart';
import '../providers/watchlist_store.dart';
import '../providers/download_store.dart';
import '../models/download_item.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/comment_item.dart';
import '../services/supabase_manager.dart';
import '../services/auth_session.dart';

import '../app_colors.dart';
import '../app_settings.dart';
import '../player/player_screen.dart';

class DetailsScreen extends StatefulWidget {
  final String itemId;
  const DetailsScreen({super.key, required this.itemId});
  @override State<DetailsScreen> createState() => _DetailsScreenState();
}

class _DetailsScreenState extends State<DetailsScreen> {
  MediaDetails? _details;
  bool _loading = true;
  String _selectedSeason = '';
  // Comments
  List<CommentItem> _comments = [];
  bool _commentsLoaded = false;
  final _commentCtrl = TextEditingController();
  bool _postingComment = false;

  @override void dispose() {
    _commentCtrl.dispose();
    super.dispose();
  }
  bool _showAddToList = false;

  @override void initState() {
    super.initState();
    _fetchDetails();
  }

  Future<void> _fetchDetails() async {
    final scraper = context.read<MovieScraper>();
    final d = await scraper.fetchDetails(widget.itemId);
    if (mounted) setState(() { _details = d; _loading = false;
      if (d.sortedSeasons.isNotEmpty) _selectedSeason = d.sortedSeasons.first; });
  }

  void _playMovie(MediaDetails d) {
    String fix(String u) {
      if (u.isEmpty) return '';
      if (u.startsWith('http')) return u;
      return u; // URLs must be absolute from cee.buzz
    }
    Navigator.push(context, MaterialPageRoute(builder: (_) => PlayerScreen(
      itemId: widget.itemId, itemTitle: d.title, itemImageUrl: d.imageUrl,
      isMovie: true,
      videoUrl: fix(d.movieUrl), videoUrl720: fix(d.movieUrl720),
      videoUrl1080: fix(d.movieUrl1080), videoUrl360: fix(d.movieUrl360),
      videoUrl4k: fix(d.movieUrl4k),
      subtitleUrl: d.movieSubtitleUrl, subtitleVttUrl: d.movieSubtitleVttUrl,
      episodeId: widget.itemId, episodeTitle: d.title,
    )));
  }

  void _playEpisode(MediaDetails d, EpisodeItem ep) {
    String fix(String u) {
      if (u.isEmpty) return '';
      if (u.startsWith('http')) return u;
      return u; // URLs must be absolute from cee.buzz
    }
    Navigator.push(context, MaterialPageRoute(builder: (_) => PlayerScreen(
      itemId: widget.itemId, itemTitle: d.title, itemImageUrl: d.imageUrl,
      isMovie: false,
      videoUrl: fix(ep.url), videoUrl720: fix(ep.url720),
      videoUrl1080: fix(ep.url1080), videoUrl360: fix(ep.url360),
      videoUrl4k: fix(ep.url4k),
      subtitleUrl: ep.subtitleUrl, subtitleVttUrl: ep.subtitleVttUrl,
      episodeId: ep.id, episodeTitle: ep.title,
      episodes: d.episodes,
    )));
  }

  @override Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: appBg(),
      body: _loading
          ? Center(child: CircularProgressIndicator(color: utRed()))
          : _details == null
              ? Center(child: Text(L('فشل التحميل', 'Load failed'),
                  style: const TextStyle(color: Colors.white)))
              : _buildBody(_details!),
    );
  }

  Widget _buildBody(MediaDetails d) {
    final favStore = context.watch<FavoritesStore>();
    final listStore = context.watch<WatchlistStore>();
    final isFav = favStore.isFavorite(widget.itemId);
    final item = VideoItem(
      id: widget.itemId, title: d.title, imageUrl: d.imageUrl, type: 'post');

    return CustomScrollView(slivers: [
      // Hero image + back button
      SliverAppBar(
        expandedHeight: 300, pinned: true,
        backgroundColor: appBg(), elevation: 0,
        flexibleSpace: FlexibleSpaceBar(
          background: Stack(fit: StackFit.expand, children: [
            CachedNetworkImage(
              imageUrl: d.imageUrl, fit: BoxFit.cover,
              placeholder: (_, __) => Container(color: const Color(0x1AFFFFFF)),
              errorWidget: (_, __, ___) => Container(color: const Color(0x1AFFFFFF),
                child: const Icon(Icons.movie, size: 60, color: Colors.white24)),
            ),
            Container(decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter, end: Alignment.bottomCenter,
                colors: [Colors.transparent, appBg()],
              ),
            )),
          ]),
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          IconButton(
            icon: Icon(isFav ? Icons.favorite : Icons.favorite_border,
              color: isFav ? utRed() : Colors.white),
            onPressed: () => favStore.toggle(item),
          ),
          IconButton(
            icon: const Icon(Icons.bookmark_add_outlined, color: Colors.white),
            onPressed: () => _showAddToListDialog(context, item),
          ),
        ],
      ),

      SliverToBoxAdapter(child: Padding(
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 80),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // Title
          Text(d.title, style: appFontStyle(22, bold: true)),
          const SizedBox(height: 10),

          // Metadata badges
          Wrap(spacing: 8, runSpacing: 6, children: [
            if (d.year.isNotEmpty) _badge(d.year),
            if (d.genre.isNotEmpty) _badge(d.genre),
            if (d.rating.isNotEmpty) _badge('⭐ ${d.rating}'),
            if (d.runtime.isNotEmpty) _badge(d.runtime),
            _badge(d.isMovie ? L('فيلم', 'Movie') : L('مسلسل', 'Series')),
          ]),
          const SizedBox(height: 20),

          // Action buttons row
          Row(children: [
            Expanded(child: ElevatedButton.icon(
              style: ElevatedButton.styleFrom(
                backgroundColor: utRed(), padding: const EdgeInsets.symmetric(vertical: 14)),
              icon: const Icon(Icons.play_arrow),
              label: Text(d.isMovie ? L('تشغيل', 'Play') : L('أول حلقة', 'First Episode'),
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
              onPressed: () {
                if (d.isMovie) { _playMovie(d); }
                else if (d.episodes.isNotEmpty) { _playEpisode(d, d.episodes.first); }
              },
            )),
            const SizedBox(width: 12),
            _actionIconBtn(
              isFav ? Icons.favorite : Icons.favorite_border,
              L('مفضلة', 'Favourite'),
              () => favStore.toggle(item),
              color: isFav ? utRed() : null,
            ),
            const SizedBox(width: 8),
            _actionIconBtn(Icons.playlist_add, L('قائمة', 'List'),
              () => _showAddToListDialog(context, item)),
            const SizedBox(width: 8),
            _actionIconBtn(Icons.download_outlined, L('تحميل', 'Download'),
              () => _downloadUrl(d.isMovie ? d.movieUrl : (d.episodes.isNotEmpty ? d.episodes.first.url : ''))),
          ]),
          const SizedBox(height: 20),

          // Synopsis
          if (d.synopsis.isNotEmpty) ...[
            Text(L('القصة', 'Synopsis'),
              style: appFontStyle(16, bold: true, color: Colors.white70)),
            const SizedBox(height: 8),
            Text(d.synopsis,
              style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.6)),
            const SizedBox(height: 20),
          ],

          // Series episodes
          if (!d.isMovie && d.episodes.isNotEmpty) ...[
            // Season picker
            if (d.sortedSeasons.length > 1)
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(children: d.sortedSeasons.map((s) =>
                  GestureDetector(
                    onTap: () => setState(() => _selectedSeason = s),
                    child: Container(
                      margin: const EdgeInsets.only(right: 8),
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 7),
                      decoration: BoxDecoration(
                        color: _selectedSeason == s ? utRed() : Colors.white.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: _selectedSeason == s
                            ? utRed() : Colors.white.withOpacity(0.15)),
                      ),
                      child: Text(s, style: TextStyle(
                        color: Colors.white,
                        fontWeight: _selectedSeason == s ? FontWeight.w700 : FontWeight.w400,
                      )),
                    ),
                  )).toList()),
              ),
            const SizedBox(height: 14),

            // Episodes list for selected season
            ...(() {
              final eps = _selectedSeason.isEmpty
                  ? d.episodes
                  : (d.seasonsDict[_selectedSeason] ?? []);
              return eps.map((ep) => _episodeTile(d, ep)).toList();
            })(),
          ],

          // -- Comments -----------------------------------------------
          const SizedBox(height: 28),
          _buildCommentsSection(),
        ]),
      )),
    ]);
  }

  Future<void> _loadComments() async {
    if (_commentsLoaded) return;
    setState(() => _commentsLoaded = true);
    final list = await SupabaseManager.instance.fetchComments(widget.itemId);
    if (mounted) setState(() => _comments = list);
  }

  Widget _buildCommentsSection() {
    final isLoggedIn = AuthSession.instance.isLoggedIn;
    if (!_commentsLoaded) _loadComments();
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Row(children: [
        Text(L('التعليقات', 'Comments'),
          style: appFontStyle(16, bold: true)),
        const SizedBox(width: 8),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
          decoration: BoxDecoration(
            color: utRed().withOpacity(0.15),
            borderRadius: BorderRadius.circular(10)),
          child: Text('${_comments.length}',
            style: TextStyle(color: utRed(), fontSize: 12, fontWeight: FontWeight.w700)),
        ),
      ]),
      const SizedBox(height: 14),
      // Input box
      if (isLoggedIn) Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
        Expanded(child: TextField(
          controller: _commentCtrl,
          style: const TextStyle(color: Colors.white, fontSize: 14),
          maxLines: 3, minLines: 1,
          decoration: InputDecoration(
            hintText: L('اكتب تعليقاً...', 'Write a comment...'),
            hintStyle: const TextStyle(color: Colors.white38, fontSize: 13),
            filled: true, fillColor: Colors.white.withOpacity(0.07),
            contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
          ),
        )),
        const SizedBox(width: 8),
        GestureDetector(
          onTap: _postingComment ? null : () async {
            final text = _commentCtrl.text.trim();
            if (text.isEmpty) return;
            setState(() => _postingComment = true);
            final ok = await SupabaseManager.instance.postComment(widget.itemId, text);
            if (ok) {
              _commentCtrl.clear();
              final list = await SupabaseManager.instance.fetchComments(widget.itemId);
              if (mounted) setState(() { _comments = list; _postingComment = false; });
            } else {
              if (mounted) setState(() => _postingComment = false);
            }
          },
          child: Container(
            width: 42, height: 42,
            decoration: BoxDecoration(color: utRed(), shape: BoxShape.circle),
            child: _postingComment
                ? const Padding(padding: EdgeInsets.all(10),
                    child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                : const Icon(Icons.send, color: Colors.white, size: 20),
          ),
        ),
      ]) else Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: Text(L('سجّل الدخول للتعليق', 'Sign in to comment'),
          style: const TextStyle(color: Colors.white38, fontSize: 13)),
      ),
      const SizedBox(height: 16),
      // Comments list
      if (_comments.isEmpty && _commentsLoaded)
        Center(child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 20),
          child: Text(L('لا توجد تعليقات بعد', 'No comments yet'),
            style: const TextStyle(color: Colors.white38, fontSize: 14)),
        ))
      else
        ..._comments.map((c) => _commentTile(c)),
    ]);
  }

  Widget _commentTile(CommentItem c) {
    final isOwn = AuthSession.instance.user?.id == c.userId;
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white.withOpacity(0.07)),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          CircleAvatar(
            radius: 14,
            backgroundColor: utRed().withOpacity(0.2),
            child: Text(c.displayName.isNotEmpty ? c.displayName[0].toUpperCase() : '?',
              style: TextStyle(fontSize: 12, color: utRed(), fontWeight: FontWeight.w700)),
          ),
          const SizedBox(width: 8),
          Expanded(child: Text(c.displayName,
            style: const TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w600))),
          if (isOwn) GestureDetector(
            onTap: () async {
              final ok = await SupabaseManager.instance.deleteComment(c.id);
              if (ok && mounted) setState(() => _comments.removeWhere((x) => x.id == c.id));
            },
            child: const Icon(Icons.delete_outline, color: Colors.red, size: 16),
          ),
        ]),
        const SizedBox(height: 6),
        Text(c.text, style: const TextStyle(color: Colors.white, fontSize: 14, height: 1.4)),
      ]),
    );
  }

  Widget _episodeTile(MediaDetails d, EpisodeItem ep) {
    final prog = context.read<WatchProgressStore>()
        .progressFor(widget.itemId, episodeId: ep.id);
    final pct = (prog != null && prog.durationSeconds > 0)
        ? prog.progressSeconds / prog.durationSeconds : 0.0;
    return GestureDetector(
      onTap: () => _playEpisode(d, ep),
      child: Container(
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.05),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.white.withOpacity(0.08)),
        ),
        child: Row(children: [
          // Play icon
          Container(
            width: 44, height: 44,
            decoration: BoxDecoration(color: utRed().withOpacity(0.15), shape: BoxShape.circle),
            child: Icon(Icons.play_arrow, color: utRed()),
          ),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(ep.title,
              style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600),
              maxLines: 2, overflow: TextOverflow.ellipsis),
            if (pct > 0) ...[
              const SizedBox(height: 6),
              LinearProgressIndicator(
                value: pct.clamp(0, 1), minHeight: 2,
                backgroundColor: Colors.white12,
                valueColor: AlwaysStoppedAnimation<Color>(utRed()),
              ),
            ],
          ])),
          GestureDetector(
            onTap: () => _downloadUrl(ep.url, ep: ep),
            child: const Padding(
              padding: EdgeInsets.symmetric(horizontal: 6),
              child: Icon(Icons.download_outlined, color: Colors.white54, size: 20),
            ),
          ),
          const Icon(Icons.chevron_right, color: Colors.white38),
        ]),
      ),
    );
  }

  Widget _badge(String text) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
    decoration: BoxDecoration(
      color: utRed().withOpacity(0.12),
      borderRadius: BorderRadius.circular(20),
      border: Border.all(color: utRed().withOpacity(0.3)),
    ),
    child: Text(text, style: TextStyle(
      color: utRed(), fontSize: 11, fontWeight: FontWeight.w700, fontFamily: 'ExpoArabic')),
  );

  Widget _actionIconBtn(IconData icon, String label, VoidCallback onTap, {Color? color}) =>
    GestureDetector(
      onTap: onTap,
      child: Column(children: [
        Icon(icon, color: color ?? Colors.white, size: 24),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(color: Colors.white70, fontSize: 11)),
      ]),
    );

  Future<void> _downloadUrl(String url, {EpisodeItem? ep}) async {
    if (url.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(L('رابط التحميل غير متاح', 'Download URL not available'))));
      return;
    }
    final d = _details!;
    final epId  = ep?.id   ?? widget.itemId;
    final title = ep?.title ?? d.title;
    final dlId  = '${widget.itemId}_$epId';

    final store = context.read<DownloadStore>();
    if (store.hasDownload(dlId)) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(L('موجود في التحميلات', 'Already in downloads'))));
      return;
    }

    store.startDownload(DownloadItem(
      id: dlId, itemId: widget.itemId, episodeId: epId,
      title: title, imageUrl: d.imageUrl, url: url,
    ));

    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      backgroundColor: utRed(),
      content: Text(L('بدأ التحميل: $title', 'Downloading: $title'),
        style: const TextStyle(color: Colors.white)),
    ));
  }

  void _showAddToListDialog(BuildContext ctx, VideoItem item) {
    showModalBottomSheet(
      context: ctx,
      backgroundColor: const Color(0xFF1A1A1A),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (_) => _AddToListSheet(item: item),
    );
  }
}

class _AddToListSheet extends StatefulWidget {
  final VideoItem item;
  const _AddToListSheet({required this.item});
  @override State<_AddToListSheet> createState() => _AddToListSheetState();
}

class _AddToListSheetState extends State<_AddToListSheet> {
  @override Widget build(BuildContext context) {
    final store = context.watch<WatchlistStore>();
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        Text(L('أضف إلى قائمة', 'Add to List'),
          style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w700)),
        const SizedBox(height: 16),
        ListTile(
          leading: Container(
            width: 50, height: 50,
            decoration: BoxDecoration(color: utRed().withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
            child: Icon(Icons.add, color: utRed()),
          ),
          title: Text(L('إنشاء قائمة جديدة', 'Create New List'),
            style: TextStyle(color: utRed(), fontWeight: FontWeight.w700)),
          onTap: () { Navigator.pop(context); _createListDialog(context); },
        ),
        ...store.lists.map((list) {
          final added = list.items.any((i) => i.id == widget.item.id);
          return ListTile(
            leading: const Icon(Icons.playlist_play, color: Colors.white54),
            title: Text(list.name, style: const TextStyle(color: Colors.white)),
            trailing: added ? Icon(Icons.check, color: utRed()) : null,
            onTap: () {
              if (added) { store.removeItem(widget.item.id, list.id); }
              else { store.addItem(widget.item, list.id); }
              setState(() {});
            },
          );
        }),
        const SizedBox(height: 8),
      ]),
    );
  }

  void _createListDialog(BuildContext ctx) {
    final ctrl = TextEditingController();
    showDialog(context: ctx, builder: (_) => AlertDialog(
      backgroundColor: const Color(0xFF1A1A1A),
      title: Text(L('قائمة جديدة', 'New List'), style: const TextStyle(color: Colors.white)),
      content: TextField(controller: ctrl,
        style: const TextStyle(color: Colors.white),
        decoration: InputDecoration(
          hintText: L('اسم القائمة', 'List name'), hintStyle: const TextStyle(color: Colors.grey),
          enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: utRed())),
          focusedBorder: UnderlineInputBorder(borderSide: BorderSide(color: utRed())),
        )),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx),
          child: Text(L('إلغاء', 'Cancel'), style: const TextStyle(color: Colors.grey))),
        TextButton(
          onPressed: () {
            final n = ctrl.text.trim();
            if (n.isNotEmpty) {
              ctx.read<WatchlistStore>().createList(n);
              Navigator.pop(ctx);
            }
          },
          child: Text(L('إنشاء', 'Create'), style: TextStyle(color: utRed())),
        ),
      ],
    ));
  }
}
""")

print("✅ details_screen.dart written")

# --- lib/screens/settings_screen.dart ---------------------------------------
# --- lib/screens/downloads_screen.dart --------------------------------------
w("lib/screens/downloads_screen.dart", r"""import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../providers/download_store.dart';
import '../models/download_item.dart';
import '../app_colors.dart';
import '../app_settings.dart';
import '../player/player_screen.dart';
import '../models/media_details.dart';

class DownloadsScreen extends StatelessWidget {
  const DownloadsScreen({super.key});

  @override Widget build(BuildContext context) {
    return Consumer<DownloadStore>(builder: (_, store, __) {
      final items = store.items;
      return Scaffold(
        backgroundColor: appBg(),
        appBar: AppBar(
          backgroundColor: appBg(),
          title: Text(L("التحميلات", "Downloads"),
            style: appFontStyle(18, bold: true)),
          actions: [
            if (store.completed.isNotEmpty)
              TextButton(
                onPressed: () => _confirmClearAll(context, store),
                child: Text(L("حذف الكل", "Clear all"),
                  style: const TextStyle(color: Colors.red, fontSize: 13)),
              ),
          ],
        ),
        body: items.isEmpty
            ? Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
                Icon(Icons.download_outlined, size: 64, color: Colors.white24),
                const SizedBox(height: 16),
                Text(L("لا توجد تحميلات", "No downloads yet"),
                  style: const TextStyle(color: Colors.white38, fontSize: 16)),
              ]))
            : ListView.builder(
                padding: const EdgeInsets.all(12),
                itemCount: items.length,
                itemBuilder: (_, i) => _DownloadTile(item: items[i]),
              ),
      );
    });
  }

  void _confirmClearAll(BuildContext ctx, DownloadStore store) {
    showDialog(context: ctx, builder: (_) => AlertDialog(
      backgroundColor: const Color(0xFF1C1C1C),
      title: Text(L("حذف الكل؟", "Delete all?"),
        style: const TextStyle(color: Colors.white)),
      content: Text(L("سيتم حذف جميع الملفات المحملة",
        "All downloaded files will be deleted"),
        style: const TextStyle(color: Colors.white70)),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx),
          child: Text(L("إلغاء", "Cancel"), style: const TextStyle(color: Colors.white54))),
        TextButton(
          onPressed: () {
            Navigator.pop(ctx);
            for (final item in store.completed.toList()) {
              store.deleteDownload(item.id);
            }
          },
          child: const Text("OK", style: TextStyle(color: Colors.red)),
        ),
      ],
    ));
  }
}

class _DownloadTile extends StatelessWidget {
  final DownloadItem item;
  const _DownloadTile({required this.item});

  @override Widget build(BuildContext context) {
    final done = item.status == DownloadStatus.completed;
    final fail = item.status == DownloadStatus.failed ||
                 item.status == DownloadStatus.cancelled;
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(children: [
        // Thumbnail
        ClipRRect(
          borderRadius: BorderRadius.circular(8),
          child: Image.network(item.imageUrl, width: 60, height: 84,
            fit: BoxFit.cover,
            errorBuilder: (_, __, ___) => Container(
              width: 60, height: 84, color: Colors.white10,
              child: const Icon(Icons.movie, color: Colors.white24))),
        ),
        const SizedBox(width: 12),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(item.title,
            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600, fontSize: 14),
            maxLines: 2, overflow: TextOverflow.ellipsis),
          const SizedBox(height: 6),
          if (item.status == DownloadStatus.downloading) ...[
            LinearProgressIndicator(
              value: item.progress,
              backgroundColor: Colors.white12,
              color: utRed(),
              borderRadius: BorderRadius.circular(4),
            ),
            const SizedBox(height: 4),
            Text(_formatBytes(item.downloadedBytes) + ' / ' + _formatBytes(item.totalBytes),
              style: const TextStyle(color: Colors.white54, fontSize: 11)),
          ] else if (done)
            Text(L("مكتمل · ", "Done · ") + _formatBytes(item.totalBytes),
              style: const TextStyle(color: Colors.green, fontSize: 12))
          else if (fail)
            Text(L("فشل التحميل", "Download failed"),
              style: const TextStyle(color: Colors.red, fontSize: 12))
          else
            Text(L("في الانتظار...", "Queued..."),
              style: const TextStyle(color: Colors.white38, fontSize: 12)),
        ])),
        const SizedBox(width: 8),
        // Actions
        Column(children: [
          if (done) ...[
            IconButton(
              icon: Icon(Icons.play_circle_fill, color: utRed(), size: 28),
              tooltip: L("تشغيل", "Play"),
              onPressed: () => _playLocal(context, item),
            ),
            IconButton(
              icon: const Icon(Icons.delete_outline, color: Colors.red, size: 22),
              tooltip: L("حذف", "Delete"),
              onPressed: () => context.read<DownloadStore>().deleteDownload(item.id),
            ),
          ] else if (item.status == DownloadStatus.downloading)
            IconButton(
              icon: const Icon(Icons.cancel_outlined, color: Colors.orange, size: 26),
              tooltip: L("إلغاء", "Cancel"),
              onPressed: () => context.read<DownloadStore>().cancelDownload(item.id),
            )
          else if (fail)
            IconButton(
              icon: Icon(Icons.refresh, color: utRed(), size: 26),
              tooltip: L("إعادة", "Retry"),
              onPressed: () => context.read<DownloadStore>().retryDownload(item.id),
            ),
        ]),
      ]),
    );
  }

  void _playLocal(BuildContext context, DownloadItem item) {
    final mode = AppSettings.instance.downloadOpenMode;
    if (mode == 'external') {
      final uri = Uri.file(item.filePath);
      launchUrl(uri, mode: LaunchMode.externalApplication).catchError((_) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text(L('تعذر فتح الملف بمشغل خارجي', 'Could not open with external player'))));
      });
      return;
    }
    Navigator.push(context, MaterialPageRoute(builder: (_) => PlayerScreen(
      itemId: item.itemId,
      itemTitle: item.title,
      itemImageUrl: item.imageUrl,
      isMovie: item.isMovie,
      videoUrl: item.filePath,
      videoUrl720: '', videoUrl1080: '', videoUrl360: '', videoUrl4k: '',
      subtitleUrl: '', subtitleVttUrl: '',
      episodeId: item.episodeId, episodeTitle: item.title,
      episodes: const [],
    )));
  }

  String _formatBytes(int bytes) {
    if (bytes <= 0) return '0 B';
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)} KB';
    if (bytes < 1024 * 1024 * 1024) return '${(bytes / (1024*1024)).toStringAsFixed(1)} MB';
    return '${(bytes / (1024*1024*1024)).toStringAsFixed(2)} GB';
  }
}
""")
print("✅ downloads_screen.dart written")

w("lib/screens/settings_screen.dart", r"""import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/favorites_store.dart';
import '../providers/watchlist_store.dart';

import '../providers/watch_progress_store.dart';
import '../services/auth_session.dart';
import '../app_colors.dart';
import '../app_settings.dart';
import 'account_screen.dart';
import 'list_detail_screen.dart';

import 'package:cached_network_image/cached_network_image.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});
  @override State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _showMoreSettings = false;

  @override Widget build(BuildContext context) {
    final session = context.watch<AuthSession>();
    final favStore = context.watch<FavoritesStore>();
    final listStore = context.watch<WatchlistStore>();
    final progStore = context.watch<WatchProgressStore>();
    final settings = AppSettings.instance;

    return Scaffold(
      backgroundColor: appBg(),
      appBar: AppBar(
        backgroundColor: appBg(), elevation: 0,
        title: Text(L('المزيد', 'More'), style: appFontStyle(20, bold: true)),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings_outlined, color: Colors.white),
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const MoreSettingsView())),
          ),
        ],
      ),
      body: ListView(padding: const EdgeInsets.symmetric(horizontal: 20), children: [
        // Account section
        GestureDetector(
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AccountScreen())),
          child: Container(
            padding: const EdgeInsets.all(16),
            margin: const EdgeInsets.symmetric(vertical: 10),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.06),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.white.withOpacity(0.08)),
            ),
            child: Row(children: [
              CircleAvatar(
                radius: 28,
                backgroundColor: utRed().withOpacity(0.2),
                backgroundImage: (session.isLoggedIn && session.user!.avatarUrl.isNotEmpty)
                    ? CachedNetworkImageProvider(session.user!.avatarUrl) : null,
                child: (session.isLoggedIn && session.user!.avatarUrl.isEmpty)
                    ? Text(session.user!.displayName.isNotEmpty
                        ? session.user!.displayName[0].toUpperCase() : '?',
                        style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700, color: utRed()))
                    : null,
              ),
              const SizedBox(width: 14),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(
                  session.isLoggedIn ? session.user!.displayName : L('ضيف', 'Guest'),
                  style: appFontStyle(16, bold: true),
                ),
                Text(
                  session.isLoggedIn
                      ? (session.user!.email ?? '')
                      : L('اضغط لتسجيل الدخول', 'Tap to sign in'),
                  style: const TextStyle(color: Colors.white54, fontSize: 13),
                ),
              ])),
              const Icon(Icons.chevron_right, color: Colors.white38),
            ]),
          ),
        ),

        // Stats row
        Container(
          padding: const EdgeInsets.all(16),
          margin: const EdgeInsets.only(bottom: 20),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.04),
            borderRadius: BorderRadius.circular(14),
          ),
          child: Row(children: [
            _statCell(favStore.items.length, L('المفضلة', 'Favourites')),
            _divider(),
            _statCell(listStore.lists.length, L('القوائم', 'Lists')),
            _divider(),
            _statCell(progStore.allEpisodes.length, L('المشاهدة', 'Watched')),
          ]),
        ),

        // Watch Lists
        _sectionHeader(L('قوائم المشاهدة', 'Watch Lists')),
        SizedBox(
          height: 140,
          child: listStore.lists.isEmpty
              ? Center(child: Text(L('لا توجد قوائم بعد', 'No lists yet'),
                  style: const TextStyle(color: Colors.white38)))
              : ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: listStore.lists.length,
                  itemBuilder: (_, i) {
                    final list = listStore.lists[i];
                    return GestureDetector(
                      onTap: () => Navigator.push(context, MaterialPageRoute(
                        builder: (_) => ListDetailScreen(list: list))),
                      child: Container(
                        width: 120, margin: const EdgeInsets.only(right: 12),
                        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                          Container(
                            height: 90, decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.07),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            child: Center(child: Icon(
                              list.isPrivate ? Icons.lock : Icons.playlist_play,
                              color: Colors.white38, size: 28)),
                          ),
                          const SizedBox(height: 6),
                          Text(list.name, style: const TextStyle(color: Colors.white, fontSize: 12,
                            fontWeight: FontWeight.w600), maxLines: 1, overflow: TextOverflow.ellipsis),
                          Text('${list.items.length} ${L("عنصر", "items")}',
                            style: const TextStyle(color: Colors.white38, fontSize: 10)),
                        ]),
                      ),
                    );
                  },
                ),
        ),
        const SizedBox(height: 8),
        OutlinedButton.icon(
          style: OutlinedButton.styleFrom(side: BorderSide(color: utRed().withOpacity(0.4))),
          icon: Icon(Icons.add, color: utRed()),
          label: Text(L('إنشاء قائمة', 'Create List'), style: TextStyle(color: utRed())),
          onPressed: () => _createListDialog(context),
        ),
        const SizedBox(height: 20),

        // Favourites
        _sectionHeader(L('المفضلة', 'Favourites')),
        if (favStore.items.isEmpty)
          Padding(padding: const EdgeInsets.symmetric(vertical: 16),
            child: Text(L('لا توجد مفضلات', 'No favourites'),
              style: const TextStyle(color: Colors.white38)))
        else
          SizedBox(height: 120, child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: favStore.items.length,
            itemBuilder: (_, i) {
              final item = favStore.items[i];
              return GestureDetector(
                onTap: () {},
                child: Container(
                  width: 80, height: 110, margin: const EdgeInsets.only(right: 10),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(8),
                    color: Colors.white12,
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(item.imageUrl, fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => const Icon(Icons.movie, color: Colors.white24)),
                  ),
                ),
              );
            },
          )),
        const SizedBox(height: 80),
      ]),
    );
  }

  Widget _statCell(int count, String label) => Expanded(child: Column(children: [
    Text('$count', style: appFontStyle(18, bold: true)),
    Text(label, style: const TextStyle(color: Colors.grey, fontSize: 11)),
  ]));

  Widget _divider() => Container(height: 30, width: 1, color: Colors.white12);

  Widget _sectionHeader(String title) => Padding(
    padding: const EdgeInsets.fromLTRB(0, 10, 0, 12),
    child: Text(title, style: appFontStyle(17, bold: true)),
  );

  void _createListDialog(BuildContext ctx) {
    final ctrl = TextEditingController();
    showDialog(context: ctx, builder: (_) => AlertDialog(
      backgroundColor: const Color(0xFF1A1A1A),
      title: Text(L('قائمة جديدة', 'New List'), style: const TextStyle(color: Colors.white)),
      content: TextField(controller: ctrl,
        style: const TextStyle(color: Colors.white),
        decoration: InputDecoration(
          hintText: L('اسم القائمة', 'List name'), hintStyle: const TextStyle(color: Colors.grey),
          enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: utRed())),
          focusedBorder: UnderlineInputBorder(borderSide: BorderSide(color: utRed())),
        )),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx),
          child: Text(L('إلغاء', 'Cancel'), style: const TextStyle(color: Colors.grey))),
        TextButton(
          onPressed: () {
            final n = ctrl.text.trim();
            if (n.isNotEmpty) { ctx.read<WatchlistStore>().createList(n); Navigator.pop(ctx); }
          },
          child: Text(L('إنشاء', 'Create'), style: TextStyle(color: utRed())),
        ),
      ],
    ));
  }
}

// --- More Settings overlay -------------------------------------------------
class MoreSettingsView extends StatelessWidget {
  const MoreSettingsView({super.key});
  @override Widget build(BuildContext context) {
    final s = AppSettings.instance;
    return Scaffold(
      backgroundColor: appBg(),
      appBar: AppBar(
        backgroundColor: appBg(), elevation: 0,
        title: Text(L('الإعدادات', 'Settings'), style: appFontStyle(18, bold: true)),
        leading: IconButton(icon: const Icon(Icons.close, color: Colors.white),
          onPressed: () => Navigator.pop(context)),
      ),
      body: StatefulBuilder(builder: (ctx, setSt) => ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _section(L('اللغة', 'Language'), [
            _picker(['ar', 'en'], ['العربية', 'English'], s.appLanguage,
              (v) { s.appLanguage = v; setSt(() {}); }),
          ]),
          _section(L('الثيم', 'Theme'), [
            _picker(['amoled', 'dark_blue', 'dark_purple'],
              ['AMOLED Black', 'Dark Blue', 'Dark Purple'],
              s.appTheme, (v) { s.appTheme = v; setSt(() {}); }),
          ]),
          _section(L('لون التمييز', 'Accent Color'), [
            Wrap(spacing: 10, children: {
              'red': const Color(0xFFE30A14),
              'blue': const Color(0xFF1A66E6),
              'orange': const Color(0xFFF27A0D),
              'green': const Color(0xFF1AC759),
              'pink': const Color(0xFFE6338C),
            }.entries.map((e) => GestureDetector(
              onTap: () { s.accentColorName = e.key; setSt(() {}); },
              child: Container(
                width: 32, height: 32,
                decoration: BoxDecoration(
                  color: e.value, shape: BoxShape.circle,
                  border: s.accentColorName == e.key
                      ? Border.all(color: Colors.white, width: 2.5) : null,
                ),
              ),
            )).toList()),
          ]),
          _section(L('التشغيل التلقائي', 'Autoplay'), [
            SwitchListTile(
              title: Text(L('تشغيل الحلقة التالية', 'Play Next Episode'),
                style: const TextStyle(color: Colors.white)),
              value: s.autoPlayNextEnabled, activeColor: utRed(),
              onChanged: (v) { s.autoPlayNextEnabled = v; setSt(() {}); },
            ),
            if (s.autoPlayNextEnabled) Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(children: [
                Text(L('عداد: ${s.autoPlayCountdownSeconds}s',
                  'Countdown: ${s.autoPlayCountdownSeconds}s'),
                  style: const TextStyle(color: Colors.white70, fontSize: 13)),
                Expanded(child: Slider(
                  value: s.autoPlayCountdownSeconds.toDouble(), min: 3, max: 20,
                  divisions: 17, activeColor: utRed(), inactiveColor: Colors.white24,
                  onChanged: (v) { s.autoPlayCountdownSeconds = v.round(); setSt(() {}); },
                )),
              ]),
            ),
          ]),
          _section(L('التنزيل / الفتح', 'Download / Open'), [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
              child: Text(L('فتح الفيديو عبر', 'Open video via'),
                style: const TextStyle(color: Colors.white70, fontSize: 13)),
            ),
            _picker(
              ['internal', 'external'],
              [L('مشغل التطبيق', 'App Player'), L('مشغل خارجي', 'External')],
              s.downloadOpenMode,
              (v) { s.downloadOpenMode = v; setSt(() {}); },
            ),
            ListTile(
              leading: const Icon(Icons.folder_outlined, color: Colors.white54),
              title: Text(L('مجلد التنزيل', 'Download folder'),
                style: const TextStyle(color: Colors.white, fontSize: 14)),
              subtitle: Text(
                s.downloadPath.isNotEmpty ? s.downloadPath
                    : '/storage/emulated/0/Download/UTan',
                style: const TextStyle(color: Colors.white38, fontSize: 11),
                overflow: TextOverflow.ellipsis),
            ),
          ]),
          _section(L('البيانات', 'Data'), [
            ListTile(
              leading: const Icon(Icons.delete_outline, color: Colors.red),
              title: Text(L('مسح الكاش', 'Clear Cache'),
                style: const TextStyle(color: Colors.white)),
              onTap: () { s.clearCache(); ScaffoldMessenger.of(ctx)
                .showSnackBar(SnackBar(content: Text(L('تم المسح', 'Cleared')))); },
            ),
          ]),
        ],
      )),
    );
  }

  Widget _section(String title, List<Widget> children) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Padding(padding: const EdgeInsets.fromLTRB(0, 16, 0, 8),
        child: Text(title, style: TextStyle(color: utRed(), fontSize: 13,
          fontWeight: FontWeight.w700))),
      Container(
        decoration: BoxDecoration(color: Colors.white.withOpacity(0.05),
          borderRadius: BorderRadius.circular(12)),
        child: Column(children: children),
      ),
    ],
  );

  Widget _picker(List<String> values, List<String> labels, String current, void Function(String) onTap) =>
    Padding(padding: const EdgeInsets.all(12), child: Wrap(spacing: 8, children: List.generate(
      values.length, (i) => GestureDetector(
        onTap: () => onTap(values[i]),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          decoration: BoxDecoration(
            color: current == values[i] ? utRed() : Colors.white.withOpacity(0.07),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Text(labels[i], style: TextStyle(
            color: Colors.white,
            fontWeight: current == values[i] ? FontWeight.w700 : FontWeight.w400,
          )),
        ),
      ))));
}
""")

print("✅ settings_screen.dart written")

# --- lib/screens/account_screen.dart ----------------------------------------

# --- lib/screens/oauth_webview_screen.dart ---------------------------------
w("lib/screens/oauth_webview_screen.dart", r"""import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../services/auth_session.dart';
import '../services/supabase_manager.dart';
import '../providers/favorites_store.dart';
import '../providers/watch_progress_store.dart';
import '../providers/watchlist_store.dart';

class OAuthWebViewScreen extends StatefulWidget {
  final String url;
  const OAuthWebViewScreen({super.key, required this.url});
  @override State<OAuthWebViewScreen> createState() => _OAuthWebViewScreenState();
}

class _OAuthWebViewScreenState extends State<OAuthWebViewScreen> {
  late final WebViewController _ctrl;
  bool _loading = true;

  @override void initState() {
    super.initState();
    _ctrl = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0xFF0D0D0D))
      ..setUserAgent(
        'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
      )
      ..setNavigationDelegate(NavigationDelegate(
        onPageStarted: (url) {
          if (!url.startsWith('utan://')) return;
          final uri = Uri.tryParse(url.replaceFirst('utan://', 'https://x/'));
          if (uri == null) return;
          final params = Uri.splitQueryString(
              uri.fragment.isNotEmpty ? uri.fragment : uri.query);
          final at = params['access_token'];
          final rt = params['refresh_token'] ?? '';
          if (at != null && at.isNotEmpty) _handleTokens(at, rt);
        },
        onPageFinished: (_) => setState(() => _loading = false),
      ))
      ..loadRequest(Uri.parse(widget.url));
  }

  Future<void> _handleTokens(String at, String rt) async {
    try {
      final sm = SupabaseManager.instance;
      final info = await sm.getUserFromToken(at);
      if (info == null) return;
      final meta = (info['user_metadata'] as Map<String, dynamic>?) ?? {};
      final user = SupabaseUser(
        id: info['id'] as String? ?? '',
        email: info['email'] as String?,
        userMetadata: meta,
        avatarUrl: meta['avatar_url'] as String? ?? '',
      );
      await AuthSession.instance.save(accessToken: at, refreshToken: rt, user: user);
      final favs = await sm.fetchFavorites();
      if (favs.isNotEmpty) FavoritesStore.instance.mergeFromCloud(favs);
      final prog = await sm.fetchProgress();
      if (prog.isNotEmpty) WatchProgressStore.instance.mergeFromCloud(prog);
      final profile = await sm.fetchProfile();
      if (profile != null) {
        final av = profile['avatar_url'] as String? ?? '';
        if (av.isNotEmpty) await AuthSession.instance.updateAvatarUrl(av);
      }
      AuthSession.instance.setAdmin(await sm.fetchIsAdmin());
      WatchlistStore.instance.fetchFromCloud();
      if (mounted) Navigator.pop(context, true);
    } catch (_) {
      if (mounted) Navigator.pop(context, false);
    }
  }

  @override Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0D0D),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0D0D0D),
        foregroundColor: Colors.white,
        title: const Text('Google',
            style: TextStyle(fontSize: 16, color: Colors.white)),
        leading: IconButton(
          icon: const Icon(Icons.close, color: Colors.white),
          onPressed: () => Navigator.pop(context, false),
        ),
      ),
      body: Stack(children: [
        WebViewWidget(controller: _ctrl),
        if (_loading) const Center(
            child: CircularProgressIndicator(color: Colors.red)),
      ]),
    );
  }
}
""")
print("✅ oauth_webview_screen.dart written")

w("lib/screens/account_screen.dart", r"""import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../services/auth_session.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:image_picker/image_picker.dart';
import '../services/supabase_manager.dart';
import '../providers/favorites_store.dart';
import '../providers/watch_progress_store.dart';
import '../providers/watchlist_store.dart';
import 'oauth_webview_screen.dart';

import 'details_screen.dart';
import '../app_colors.dart';
import '../app_settings.dart';
import '../models/feedback_item.dart';
import 'admin_panel_screen.dart';

class AccountScreen extends StatefulWidget {
  const AccountScreen({super.key});
  @override State<AccountScreen> createState() => _AccountScreenState();
}

class _AccountScreenState extends State<AccountScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tab;
  bool _isLogin = true;
  bool _loading = false;
  String _error = '';
  final _emailCtrl = TextEditingController();
  final _passCtrl  = TextEditingController();
  final _nameCtrl  = TextEditingController();
  bool _obscure = true;

  // Feedback
  List<FeedbackItem> _myFeedback = [];
  bool _feedbackLoading = false;
  final _fbMsgCtrl = TextEditingController();
  String _fbType = 'suggestion';

  // Profile
  String _avatarUrl = '';

  @override void initState() {
    super.initState();
    _tab = TabController(length: 3, vsync: this);
    _loadFeedback();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    if (!AuthSession.instance.isLoggedIn) return;
    final cached = AuthSession.instance.user?.avatarUrl ?? '';
    if (cached.isNotEmpty && mounted) setState(() => _avatarUrl = cached);
    final profile = await SupabaseManager.instance.fetchProfile();
    if (profile != null && mounted) {
      final url = profile['avatar_url'] as String? ?? '';
      setState(() => _avatarUrl = url);
      await AuthSession.instance.updateAvatarUrl(url);
    }
  }

  @override void dispose() {
    _tab.dispose();
    _emailCtrl.dispose(); _passCtrl.dispose();
    _nameCtrl.dispose(); _fbMsgCtrl.dispose();
    super.dispose();
  }

  Future<void> _loadFeedback() async {
    if (!AuthSession.instance.isLoggedIn) return;
    setState(() => _feedbackLoading = true);
    _myFeedback = await SupabaseManager.instance.fetchMyFeedback();
    if (mounted) setState(() => _feedbackLoading = false);
  }

  Future<void> _doAuth() async {
    final email = _emailCtrl.text.trim();
    final pass  = _passCtrl.text.trim();
    if (email.isEmpty || pass.isEmpty) { setState(() => _error = L('أدخل البريد وكلمة المرور', 'Enter email and password')); return; }
    setState(() { _loading = true; _error = ''; });
    final sm = SupabaseManager.instance;
    Map<String, dynamic>? result;
    if (_isLogin) {
      result = await sm.signIn(email: email, password: pass);
    } else {
      final name = _nameCtrl.text.trim();
      if (name.isEmpty) { setState(() { _loading = false; _error = L('أدخل اسمك', 'Enter your name'); }); return; }
      result = await sm.signUp(email: email, password: pass, displayName: name);
    }
    if (!mounted) return;
    if (result == null) { setState(() { _loading = false; _error = L('حدث خطأ', 'An error occurred'); }); return; }
    if (result.containsKey('error')) {
      setState(() { _loading = false; _error = result!['error'] as String; });
      return;
    }
    // Email confirmation required
    if (result.containsKey('needsConfirmation')) {
      setState(() => _loading = false);
      if (!mounted) return;
      showDialog(context: context, builder: (_) => AlertDialog(
        backgroundColor: const Color(0xFF1A1A1A),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Row(children: [
          Icon(Icons.mark_email_read_outlined, color: utRed()),
          const SizedBox(width: 10),
          Text(L('تحقق من بريدك', 'Verify your email'),
            style: const TextStyle(color: Colors.white, fontSize: 16)),
        ]),
        content: Text(
          L('تم إنشاء حسابك بنجاح! تم إرسال رسالة تأكيد إلى بريدك الإلكتروني. يرجى النقر على الرابط في الرسالة لتفعيل حسابك ثم تسجيل الدخول.',
            'Account created! A confirmation email has been sent. Please click the link in the email to verify your account, then sign in.'),
          style: const TextStyle(color: Colors.white70, fontSize: 13, height: 1.5)),
        actions: [
          TextButton(
            onPressed: () { Navigator.pop(context); setState(() => _isLogin = true); },
            child: Text(L('حسناً، انتقل لتسجيل الدخول', 'OK, go to sign in'),
              style: TextStyle(color: utRed())),
          ),
        ],
      ));
      return;
    }
    final userMap = result['user'] as Map<String, dynamic>? ?? {};
    final user = SupabaseUser(
      id: userMap['id'] as String? ?? '',
      email: userMap['email'] as String?,
      userMetadata: (userMap['user_metadata'] as Map<String, dynamic>?) ?? {},
    );
    await AuthSession.instance.save(
      accessToken: result['access_token'] as String,
      refreshToken: result['refresh_token'] as String,
      user: user,
    );
    // Sync cloud data
    final cloudFavs = await SupabaseManager.instance.fetchFavorites();
    if (cloudFavs.isNotEmpty && mounted) context.read<FavoritesStore>().mergeFromCloud(cloudFavs);
    final cloudProg = await SupabaseManager.instance.fetchProgress();
    if (cloudProg.isNotEmpty && mounted) context.read<WatchProgressStore>().mergeFromCloud(cloudProg);
    // Check admin
    final isAdmin = await SupabaseManager.instance.fetchIsAdmin();
    AuthSession.instance.setAdmin(isAdmin);
    // Sync watchlists + profile
    if (mounted) context.read<WatchlistStore>().fetchFromCloud();
    _loadProfile();
    setState(() => _loading = false);
    if (mounted) Navigator.pop(context);
  }

  @override Widget build(BuildContext context) {
    final session = context.watch<AuthSession>();
    return Scaffold(
      backgroundColor: appBg(),
      appBar: AppBar(
        backgroundColor: appBg(), elevation: 0,
        title: Text(L('الحساب', 'Account'), style: appFontStyle(18, bold: true)),
        leading: IconButton(icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context)),
        actions: [
          if (session.isAdmin)
            IconButton(
              icon: const Icon(Icons.admin_panel_settings, color: Colors.orange),
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AdminPanelScreen())),
            ),
        ],
      ),
      body: session.isLoggedIn ? _buildLoggedIn(session) : _buildAuth(),
    );
  }

  Future<void> _doGoogleSignIn() async {
    setState(() { _loading = true; _error = ''; });
    try {
      final oauthUrl = SupabaseManager.instance.getOAuthUrl('google');
      if (!mounted) return;
      final result = await Navigator.push<bool>(context,
        MaterialPageRoute(builder: (_) => OAuthWebViewScreen(url: oauthUrl)));
      setState(() => _loading = false);
      if (result == true && mounted) Navigator.pop(context);
    } catch (e) {
      setState(() { _loading = false; _error = e.toString(); });
    }
  }


  Widget _buildLoggedIn(AuthSession session) {
    final favs     = context.watch<FavoritesStore>();
    final progress = context.watch<WatchProgressStore>();
    final watchlist = favs; // My List uses favorites
    final name     = session.user?.displayName ?? session.user?.email?.split('@').first ?? 'User';
    final email    = session.user?.email ?? '';
    final initials = name.isNotEmpty ? name[0].toUpperCase() : 'U';

    return SingleChildScrollView(
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const SizedBox(height: 28),

        // -- Avatar + name ----------------------------------------------
        Center(child: Column(children: [
          Stack(children: [
            CircleAvatar(
              radius: 48,
              backgroundColor: utRed().withOpacity(0.15),
              backgroundImage: (_avatarUrl.isNotEmpty || session.user!.avatarUrl.isNotEmpty)
                  ? CachedNetworkImageProvider(
                      _avatarUrl.isNotEmpty ? _avatarUrl : session.user!.avatarUrl)
                  : null,
              child: (_avatarUrl.isEmpty && session.user!.avatarUrl.isEmpty)
                  ? Text(initials, style: TextStyle(fontSize: 38,
                      fontWeight: FontWeight.w700, color: utRed()))
                  : null,
            ),
            Positioned(bottom: 0, right: 0,
              child: GestureDetector(
                onTap: () => _showEditProfileSheet(context, name),
                child: Container(
                  width: 28, height: 28,
                  decoration: BoxDecoration(
                    color: utRed(), shape: BoxShape.circle,
                    border: Border.all(color: appBg(), width: 2)),
                  child: const Icon(Icons.edit, color: Colors.white, size: 14),
                ),
              )),
          ]),
          const SizedBox(height: 12),
          Text(name, style: appFontStyle(20, bold: true)),
          const SizedBox(height: 4),
          Text(email, style: const TextStyle(color: Colors.white54, fontSize: 13)),
          const SizedBox(height: 14),
          OutlinedButton(
            onPressed: () => _showEditProfileSheet(context, name),
            style: OutlinedButton.styleFrom(
              side: const BorderSide(color: Colors.white30),
              shape: const StadiumBorder(),
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8)),
            child: Text(L('تعديل الملف الشخصي', 'Edit Profile'),
              style: const TextStyle(color: Colors.white)),
          ),
        ])),

        const SizedBox(height: 24),
        const Divider(color: Colors.white12, height: 1),

        // -- Stats row -------------------------------------------------
        Row(children: [
          _statCell(favs.items.length.toString(),     L('المفضلة', 'Favorites')),
          Container(width: 1, height: 40, color: Colors.white12),
          _statCell(progress.recent.length.toString(), L('المشاهدة', 'Watched')),
          Container(width: 1, height: 40, color: Colors.white12),
          _statCell(favs.items.length.toString(), L('قائمتي', 'My List')),
        ]),

        const Divider(color: Colors.white12, height: 1),
        const SizedBox(height: 24),



        // -- Favorites ------------------------------------------------
        if (favs.items.isNotEmpty) ...[
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 18),
            child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(L('المفضلة', 'Favorites'), style: appFontStyle(16, bold: true)),
                Text('${favs.items.length} ${L("عناصر", "items")}',
                  style: const TextStyle(color: Colors.white38, fontSize: 13)),
              ]),
          ),
          const SizedBox(height: 12),
          SizedBox(
            height: 110,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 14),
              itemCount: favs.items.length,
              itemBuilder: (_, i) {
                final item = favs.items[i];
                return GestureDetector(
                  onTap: () => Navigator.push(context, MaterialPageRoute(
                    builder: (_) => DetailsScreen(itemId: item.id))),
                  child: Container(
                    width: 72, margin: const EdgeInsets.only(right: 10),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: CachedNetworkImage(
                        imageUrl: item.imageUrl, fit: BoxFit.cover,
                        placeholder: (_, __) => Container(color: Colors.white10),
                        errorWidget: (_, __, ___) => Container(color: Colors.white10),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 24),
        ],

        // -- History --------------------------------------------------
        ...[
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 18),
            child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(L('السجل', 'History'), style: appFontStyle(16, bold: true)),
                if (progress.all.isNotEmpty)
                  GestureDetector(
                    onTap: () {},
                    child: Text(
                      '${L("عرض الكل", "See All")} (${progress.recent.length}) ›',
                      style: TextStyle(color: utRed(), fontSize: 13,
                        fontWeight: FontWeight.w600)),
                  ),
              ]),
          ),
          const SizedBox(height: 12),
          if (progress.recent.isEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 18),
              child: Text(L('لا يوجد سجل', 'No history yet'),
                style: const TextStyle(color: Colors.white38)),
            )
          else
            SizedBox(
              height: 110,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 14),
                itemCount: progress.recent.length,
                itemBuilder: (_, i) {
                  final p = progress.recent[i];
                  return GestureDetector(
                    onTap: () => Navigator.push(context, MaterialPageRoute(
                      builder: (_) => DetailsScreen(itemId: p.itemId))),
                    child: Container(
                      width: 72, margin: const EdgeInsets.only(right: 10),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: Stack(fit: StackFit.expand, children: [
                          CachedNetworkImage(
                            imageUrl: p.imageUrl, fit: BoxFit.cover,
                            placeholder: (_, __) => Container(color: Colors.white10),
                            errorWidget: (_, __, ___) => Container(color: Colors.white10),
                          ),
                          if (p.percent > 0)
                            Positioned(
                              bottom: 0, left: 0, right: 0,
                              child: LinearProgressIndicator(
                                value: p.percent / 100,
                                backgroundColor: Colors.black45,
                                valueColor: AlwaysStoppedAnimation<Color>(utRed()),
                                minHeight: 3,
                              ),
                            ),
                        ]),
                      ),
                    ),
                  );
                },
              ),
            ),
        ],

        const SizedBox(height: 30),

        // -- Sign out -------------------------------------------------
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 18),
          child: TextButton.icon(
            onPressed: () async {
              await session.signOut();
              if (mounted) setState(() {});
            },
            icon: const Icon(Icons.logout, color: Colors.red),
            label: Text(L('تسجيل الخروج', 'Sign Out'),
              style: const TextStyle(color: Colors.red)),
          ),
        ),
        const SizedBox(height: 80),
      ]),
    );
  }

  Future<void> _showEditProfileSheet(BuildContext ctx, String currentName) async {
    final nameCtrl = TextEditingController(text: currentName);
    bool saving = false;
    String err = '';
    String previewUrl = _avatarUrl;
    List<int>? pickedBytes;
    String pickedExt = 'jpg';

    await showModalBottomSheet(
      context: ctx,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF1C1C1C),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (bCtx) => StatefulBuilder(
        builder: (bCtx, setSt) => Padding(
          padding: EdgeInsets.only(
            left: 20, right: 20, top: 20,
            bottom: MediaQuery.of(bCtx).viewInsets.bottom + 24),
          child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.start, children: [
            Center(child: Container(width: 40, height: 4,
              decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(2)))),
            const SizedBox(height: 16),
            Text(L('تعديل الملف الشخصي', 'Edit Profile'),
              style: appFontStyle(18, bold: true)),
            const SizedBox(height: 20),
            // Avatar preview + pick button
            Center(child: Stack(alignment: Alignment.bottomRight, children: [
              CircleAvatar(
                radius: 46,
                backgroundColor: utRed().withOpacity(0.15),
                backgroundImage: pickedBytes != null ? MemoryImage(Uint8List.fromList(pickedBytes!))
                    : (previewUrl.isNotEmpty ? CachedNetworkImageProvider(previewUrl) : null) as ImageProvider?,
                child: (pickedBytes == null && previewUrl.isEmpty)
                    ? Text(nameCtrl.text.isNotEmpty ? nameCtrl.text[0].toUpperCase() : '?',
                        style: TextStyle(fontSize: 34, color: utRed(), fontWeight: FontWeight.w700))
                    : null,
              ),
              GestureDetector(
                onTap: () async {
                  final picker = ImagePicker();
                  final img = await picker.pickImage(
                    source: ImageSource.gallery, maxWidth: 512, maxHeight: 512, imageQuality: 85);
                  if (img == null) return;
                  final bytes = await img.readAsBytes();
                  final ext = img.name.split('.').last.toLowerCase();
                  setSt(() { pickedBytes = bytes; pickedExt = ext; });
                },
                child: Container(
                  width: 30, height: 30,
                  decoration: BoxDecoration(
                    color: utRed(), shape: BoxShape.circle,
                    border: Border.all(color: const Color(0xFF1C1C1C), width: 2)),
                  child: const Icon(Icons.camera_alt, color: Colors.white, size: 16),
                ),
              ),
            ])),
            const SizedBox(height: 18),
            // Display name field
            TextField(
              controller: nameCtrl,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: L('الاسم المعروض', 'Display name'),
                hintStyle: const TextStyle(color: Colors.white38),
                prefixIcon: const Icon(Icons.person_outline, color: Colors.white38),
                filled: true, fillColor: Colors.white.withOpacity(0.07),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10), borderSide: BorderSide.none),
              ),
            ),
            if (err.isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(err, style: const TextStyle(color: Colors.red, fontSize: 13)),
            ],
            const SizedBox(height: 20),
            SizedBox(width: double.infinity, child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: utRed(),
                padding: const EdgeInsets.symmetric(vertical: 14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10))),
              onPressed: saving ? null : () async {
                setSt(() { saving = true; err = ''; });
                final uid = AuthSession.instance.user?.id;
                String? finalAvatarUrl = previewUrl;
                // Upload image if picked
                if (pickedBytes != null && uid != null) {
                  final uploaded = await SupabaseManager.instance
                      .uploadAvatar(uid, pickedBytes!, pickedExt);
                  if (uploaded != null) {
                    finalAvatarUrl = uploaded;
                  } else {
                    // Upload failed - ask user for URL instead
                    setSt(() { saving = false; });
                    if (!bCtx.mounted) return;
                    final urlCtrl = TextEditingController();
                    final manualUrl = await showDialog<String>(
                      context: bCtx,
                      builder: (dCtx) => AlertDialog(
                        backgroundColor: const Color(0xFF1C1C1C),
                        title: Text(L('تعذر رفع الصورة', 'Upload failed'),
                          style: const TextStyle(color: Colors.white, fontSize: 16)),
                        content: Column(mainAxisSize: MainAxisSize.min, children: [
                          Text(L('أدخل رابط الصورة يدوياً', 'Enter image URL manually'),
                            style: const TextStyle(color: Colors.white70, fontSize: 13)),
                          const SizedBox(height: 12),
                          TextField(
                            controller: urlCtrl, autofocus: true,
                            style: const TextStyle(color: Colors.white, fontSize: 13),
                            decoration: InputDecoration(
                              hintText: 'https://',
                              hintStyle: const TextStyle(color: Colors.white38),
                              filled: true, fillColor: Colors.white12,
                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(8),
                                borderSide: BorderSide.none)),
                          ),
                        ]),
                        actions: [
                          TextButton(onPressed: () => Navigator.pop(dCtx),
                            child: Text(L('إلغاء', 'Cancel'),
                              style: const TextStyle(color: Colors.white54))),
                          TextButton(
                            onPressed: () => Navigator.pop(dCtx, urlCtrl.text.trim()),
                            child: Text(L('حفظ', 'Save'),
                              style: TextStyle(color: utRed()))),
                        ],
                      ),
                    );
                    if (manualUrl != null && manualUrl.isNotEmpty) {
                      finalAvatarUrl = manualUrl;
                    } else {
                      return; // user cancelled
                    }
                    setSt(() { saving = true; });
                  }
                }
                final newName = nameCtrl.text.trim();
                final ok = await SupabaseManager.instance.updateProfile(
                  displayName: newName.isNotEmpty ? newName : null,
                  avatarUrl: finalAvatarUrl,
                );
                if (ok) {
                  if (newName.isNotEmpty) await AuthSession.instance.updateDisplayNameLocal(newName);
                  if (finalAvatarUrl != null) await AuthSession.instance.updateAvatarUrl(finalAvatarUrl);
                  if (mounted) setState(() => _avatarUrl = finalAvatarUrl ?? '');
                  if (bCtx.mounted) Navigator.pop(bCtx);
                } else {
                  setSt(() { saving = false; err = L('فشل الحفظ', 'Save failed'); });
                }
              },
              child: saving
                  ? const SizedBox(width: 20, height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : Text(L('حفظ', 'Save'),
                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
            )),
          ]),
        ),
      ),
    );
    nameCtrl.dispose();
  }

  Widget _statCell(String value, String label) => Expanded(
    child: Padding(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Column(children: [
        Text(value, style: appFontStyle(22, bold: true)),
        const SizedBox(height: 2),
        Text(label, style: const TextStyle(color: Colors.white54, fontSize: 12)),
      ]),
    ),
  );

  Widget _buildAuth() => SingleChildScrollView(
    padding: const EdgeInsets.all(24),
    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      const SizedBox(height: 20),
      // Toggle login/signup
      Row(children: [
        GestureDetector(
          onTap: () => setState(() { _isLogin = true; _error = ''; }),
          child: Text(L('تسجيل الدخول', 'Sign In'),
            style: TextStyle(
              fontSize: 22, fontWeight: _isLogin ? FontWeight.w700 : FontWeight.w400,
              color: _isLogin ? Colors.white : Colors.white38)),
        ),
        const SizedBox(width: 20),
        GestureDetector(
          onTap: () => setState(() { _isLogin = false; _error = ''; }),
          child: Text(L('إنشاء حساب', 'Sign Up'),
            style: TextStyle(
              fontSize: 22, fontWeight: !_isLogin ? FontWeight.w700 : FontWeight.w400,
              color: !_isLogin ? Colors.white : Colors.white38)),
        ),
      ]),
      const SizedBox(height: 30),
      if (!_isLogin) ...[
        _authField(_nameCtrl, L('الاسم', 'Name'), Icons.person_outline),
        const SizedBox(height: 16),
      ],
      _authField(_emailCtrl, L('البريد الإلكتروني', 'Email'), Icons.email_outlined,
        type: TextInputType.emailAddress),
      const SizedBox(height: 16),
      _authField(_passCtrl, L('كلمة المرور', 'Password'), Icons.lock_outline,
        obscure: _obscure, suffixIcon: IconButton(
          icon: Icon(_obscure ? Icons.visibility_off : Icons.visibility,
            color: Colors.white38),
          onPressed: () => setState(() => _obscure = !_obscure),
        )),
      const SizedBox(height: 12),
      if (_error.isNotEmpty)
        Text(_error, style: const TextStyle(color: Colors.red, fontSize: 13)),
      const SizedBox(height: 24),
      SizedBox(width: double.infinity, child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: utRed(), padding: const EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
        onPressed: _loading ? null : _doAuth,
        child: _loading
            ? const SizedBox(width: 20, height: 20,
                child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
            : Text(_isLogin ? L('دخول', 'Sign In') : L('إنشاء', 'Create'),
                style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w700)),
      )),

      // -- OR divider --------------------------------------------------
      const SizedBox(height: 16),
      Row(children: [
        const Expanded(child: Divider(color: Colors.white24)),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          child: Text(L('أو', 'OR'),
            style: const TextStyle(color: Colors.white38, fontSize: 13)),
        ),
        const Expanded(child: Divider(color: Colors.white24)),
      ]),
      const SizedBox(height: 16),

      // -- Google Sign-In button ----------------------------------------
      SizedBox(
        width: double.infinity,
        child: OutlinedButton.icon(
          onPressed: _loading ? null : _doGoogleSignIn,
          style: OutlinedButton.styleFrom(
            side: const BorderSide(color: Colors.white24),
            backgroundColor: Colors.white.withOpacity(0.06),
            padding: const EdgeInsets.symmetric(vertical: 14),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          ),
          icon: Container(
            width: 20, height: 20,
            decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.white),
            child: const Center(
              child: Text('G', style: TextStyle(
                color: Color(0xFF4285F4),
                fontSize: 13, fontWeight: FontWeight.w900)),
            ),
          ),
          label: Text(L('الدخول بـ Google', 'Continue with Google'),
            style: const TextStyle(color: Colors.white70, fontSize: 15)),
        ),
      ),
    ]),
  );

  Widget _authField(TextEditingController ctrl, String label, IconData icon,
      {bool obscure = false, TextInputType? type, Widget? suffixIcon}) =>
    TextField(
      controller: ctrl, obscureText: obscure, keyboardType: type,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        hintText: label, hintStyle: const TextStyle(color: Colors.grey),
        prefixIcon: Icon(icon, color: Colors.white38),
        suffixIcon: suffixIcon,
        filled: true, fillColor: Colors.white.withOpacity(0.08),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none),
      ),
    );

  Widget _infoTile(IconData icon, String label, String value) =>
    ListTile(
      leading: Icon(icon, color: Colors.white54),
      title: Text(label, style: const TextStyle(color: Colors.white54, fontSize: 12)),
      subtitle: Text(value, style: const TextStyle(color: Colors.white, fontSize: 15)),
    );

}
""")
print("✅ account_screen.dart written")

# --- lib/screens/admin_panel_screen.dart ------------------------------------
w("lib/screens/admin_panel_screen.dart", r"""import 'package:flutter/material.dart';
import '../services/supabase_manager.dart';
import '../models/feedback_item.dart';
import '../app_colors.dart';
import '../app_settings.dart';

class AdminPanelScreen extends StatefulWidget {
  const AdminPanelScreen({super.key});
  @override State<AdminPanelScreen> createState() => _AdminPanelScreenState();
}

class _AdminPanelScreenState extends State<AdminPanelScreen> {
  List<FeedbackItem> _items = [];
  bool _loading = true;
  String _filter = 'all';

  @override void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    _items = await SupabaseManager.instance.fetchAllFeedback();
    if (mounted) setState(() => _loading = false);
  }

  List<FeedbackItem> get _filtered {
    if (_filter == 'all') return _items;
    if (_filter == 'open') return _items.where((i) => i.status == 'open').toList();
    return _items.where((i) => i.type == _filter).toList();
  }

  @override Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: appBg(),
      appBar: AppBar(
        backgroundColor: appBg(), elevation: 0,
        title: Text(L('لوحة التحكم', 'Admin Panel'), style: appFontStyle(18, bold: true)),
      ),
      body: Column(children: [
        // Filter chips
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(children: [
              for (final f in ['all', 'open', 'suggestion', 'complaint', 'bug'])
                GestureDetector(
                  onTap: () => setState(() => _filter = f),
                  child: Container(
                    margin: const EdgeInsets.only(right: 8),
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 7),
                    decoration: BoxDecoration(
                      color: _filter == f ? utRed() : Colors.white.withOpacity(0.08),
                      borderRadius: BorderRadius.circular(20)),
                    child: Text(f, style: const TextStyle(color: Colors.white, fontSize: 13)),
                  ),
                ),
            ]),
          ),
        ),
        Expanded(child: _loading
          ? Center(child: CircularProgressIndicator(color: utRed()))
          : RefreshIndicator(
              onRefresh: _load, color: utRed(),
              child: ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _filtered.length,
                itemBuilder: (_, i) {
                  final fb = _filtered[i];
                  return Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.05),
                      borderRadius: BorderRadius.circular(12)),
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Row(children: [
                        Expanded(child: Text(fb.displayName,
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w700))),
                        _chip(fb.type, utRed()),
                        const SizedBox(width: 6),
                        PopupMenuButton<String>(
                          icon: _chip(fb.status,
                            fb.status == 'open' ? Colors.orange : Colors.green),
                          color: const Color(0xFF1A1A1A),
                          onSelected: (s) async {
                            await SupabaseManager.instance.updateFeedbackStatus(fb.id, s);
                            _load();
                          },
                          itemBuilder: (_) => ['open', 'in_progress', 'resolved', 'closed']
                              .map((s) => PopupMenuItem(value: s,
                                child: Text(s, style: const TextStyle(color: Colors.white))))
                              .toList(),
                        ),
                      ]),
                      if (fb.email != null) Text(fb.email!,
                        style: const TextStyle(color: Colors.white38, fontSize: 11)),
                      const SizedBox(height: 8),
                      Text(fb.message, style: const TextStyle(color: Colors.white70, fontSize: 13)),
                      const SizedBox(height: 6),
                      Text(fb.createdAt.substring(0, 10),
                        style: const TextStyle(color: Colors.white38, fontSize: 10)),
                    ]),
                  );
                },
              ),
          )),
      ]),
    );
  }

  Widget _chip(String text, Color color) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
    decoration: BoxDecoration(
      color: color.withOpacity(0.18), borderRadius: BorderRadius.circular(6)),
    child: Text(text, style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.w700)),
  );
}
""")

# --- lib/screens/list_detail_screen.dart -------------------------------------
w("lib/screens/list_detail_screen.dart", r"""import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:provider/provider.dart';
import '../models/watch_list.dart';
import '../providers/watchlist_store.dart';

import '../app_colors.dart';
import '../app_settings.dart';
import 'details_screen.dart';

class ListDetailScreen extends StatelessWidget {
  final WatchList list;
  const ListDetailScreen({super.key, required this.list});

  @override Widget build(BuildContext context) {
    final store = context.watch<WatchlistStore>();
    final current = store.lists.firstWhere((l) => l.id == list.id, orElse: () => list);

    return Scaffold(
      backgroundColor: appBg(),
      appBar: AppBar(
        backgroundColor: appBg(), elevation: 0,
        title: Text(current.name, style: appFontStyle(18, bold: true)),
        actions: [
          IconButton(
            icon: const Icon(Icons.edit_outlined, color: Colors.white),
            onPressed: () => _renameDialog(context, store, current),
          ),
          IconButton(
            icon: const Icon(Icons.delete_outline, color: Colors.red),
            onPressed: () async {
              final ok = await showDialog<bool>(context: context, builder: (_) => AlertDialog(
                backgroundColor: const Color(0xFF1A1A1A),
                title: Text(L('حذف القائمة؟', 'Delete List?'),
                  style: const TextStyle(color: Colors.white)),
                actions: [
                  TextButton(onPressed: () => Navigator.pop(context, false),
                    child: Text(L('إلغاء', 'Cancel'), style: const TextStyle(color: Colors.grey))),
                  TextButton(onPressed: () => Navigator.pop(context, true),
                    child: const Text('حذف', style: TextStyle(color: Colors.red))),
                ],
              ));
              if (ok == true) { store.deleteList(current.id); Navigator.pop(context); }
            },
          ),
        ],
      ),
      body: current.items.isEmpty
          ? Center(child: Text(L('القائمة فارغة', 'List is empty'),
              style: const TextStyle(color: Colors.white38)))
          : GridView.builder(
              padding: const EdgeInsets.all(16),
              gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                maxCrossAxisExtent: 150, childAspectRatio: 120 / 220,
                crossAxisSpacing: 14, mainAxisSpacing: 16),
              itemCount: current.items.length,
              itemBuilder: (_, i) {
                final item = current.items[i];
                return GestureDetector(
                  onTap: () => Navigator.push(context, MaterialPageRoute(
                    builder: (_) => DetailsScreen(itemId: item.id))),
                  onLongPress: () => store.removeItem(item.id, current.id),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Expanded(child: ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: CachedNetworkImage(
                        imageUrl: item.imageUrl, fit: BoxFit.cover,
                        placeholder: (_, __) => Container(color: Colors.white12),
                        errorWidget: (_, __, ___) => Container(color: Colors.white12,
                          child: const Icon(Icons.movie, color: Colors.white24)),
                      ),
                    )),
                    const SizedBox(height: 6),
                    Text(item.title,
                      style: const TextStyle(color: Colors.white, fontSize: 11),
                      maxLines: 2, overflow: TextOverflow.ellipsis),
                  ]),
                );
              },
            ),
    );
  }

  void _renameDialog(BuildContext ctx, WatchlistStore store, WatchList current) {
    final ctrl = TextEditingController(text: current.name);
    showDialog(context: ctx, builder: (_) => AlertDialog(
      backgroundColor: const Color(0xFF1A1A1A),
      title: Text(L('إعادة تسمية', 'Rename'), style: const TextStyle(color: Colors.white)),
      content: TextField(controller: ctrl, style: const TextStyle(color: Colors.white),
        decoration: InputDecoration(
          enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: utRed())),
          focusedBorder: UnderlineInputBorder(borderSide: BorderSide(color: utRed())),
        )),
      actions: [
        TextButton(onPressed: () => Navigator.pop(ctx),
          child: Text(L('إلغاء', 'Cancel'), style: const TextStyle(color: Colors.grey))),
        TextButton(
          onPressed: () { store.renameList(current.id, ctrl.text.trim()); Navigator.pop(ctx); },
          child: Text(L('حفظ', 'Save'), style: TextStyle(color: utRed())),
        ),
      ],
    ));
  }
}
""")

print("✅ admin + list_detail + downloads screens written")

# --- lib/screens/main_tab.dart -----------------------------------------------
w("lib/screens/main_tab.dart", r"""import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../app_colors.dart';
import '../app_settings.dart';
import '../services/auth_session.dart';
import 'home_screen.dart';
import 'browse_screen.dart';
import 'search_screen.dart';
import 'downloads_screen.dart';
import 'settings_screen.dart';

class MainTabScreen extends StatefulWidget {
  const MainTabScreen({super.key});
  @override State<MainTabScreen> createState() => _MainTabScreenState();
}

class _MainTabScreenState extends State<MainTabScreen> {
  int _current = 0;

  static const _screens = [
    HomeScreen(),
    BrowseScreen(),
    SearchScreen(),
    DownloadsScreen(),
    SettingsScreen(),
  ];

  @override Widget build(BuildContext context) {
    final bg = appBg();
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
      systemNavigationBarColor: bg,
      systemNavigationBarIconBrightness: Brightness.light,
    ));
    return Scaffold(
      backgroundColor: bg,
      body: IndexedStack(index: _current, children: _screens),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: bg,
          border: Border(top: BorderSide(color: Colors.white.withOpacity(0.06), width: 1)),
        ),
        child: NavigationBar(
          backgroundColor: Colors.transparent,
          indicatorColor: utRed().withOpacity(0.15),
          selectedIndex: _current,
          onDestinationSelected: (i) => setState(() => _current = i),
          destinations: [
            _dest(Icons.home_outlined, Icons.home, L('الرئيسية', 'Home')),
            _dest(Icons.grid_view_outlined, Icons.grid_view, L('تصفح', 'Browse')),
            _dest(Icons.search_outlined, Icons.search, L('بحث', 'Search')),
            _dest(Icons.download_outlined, Icons.download, L('تنزيل', 'Downloads')),
            _dest(Icons.more_horiz_outlined, Icons.more_horiz, L('المزيد', 'More')),
          ],
        ),
      ),
    );
  }

  NavigationDestination _dest(IconData icon, IconData selected, String label) =>
      NavigationDestination(
        icon: Icon(icon, color: Colors.white38),
        selectedIcon: Icon(selected, color: utRed()),
        label: label,
      );
}
""")

# --- lib/main.dart -----------------------------------------------------------
w("lib/main.dart", r"""import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:app_links/app_links.dart';
import 'app_settings.dart';
import 'app_colors.dart';
import 'services/scraper.dart';
import 'services/auth_session.dart';
import 'services/supabase_manager.dart';
import 'providers/favorites_store.dart';
import 'providers/watch_progress_store.dart';
import 'providers/watchlist_store.dart';
import 'providers/download_store.dart';
import 'screens/main_tab.dart';
import 'widgets/ut_loader.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  final settings = AppSettings.instance;
  await settings.init();
  await AuthSession.instance.init();
  await FavoritesStore.instance.init();
  await WatchProgressStore.instance.init();
  await WatchlistStore.instance.init();
  await DownloadStore.instance.init();
  runApp(const UTanApp());
}

class UTanApp extends StatelessWidget {
  const UTanApp({super.key});

  @override Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppSettings.instance),
        ChangeNotifierProvider(create: (_) => AuthSession.instance),
        ChangeNotifierProvider(create: (_) => MovieScraper()),
        ChangeNotifierProvider(create: (_) => FavoritesStore.instance),
        ChangeNotifierProvider(create: (_) => WatchProgressStore.instance),
        ChangeNotifierProvider(create: (_) => WatchlistStore.instance),
        ChangeNotifierProvider(create: (_) => DownloadStore.instance),
      ],
      child: Consumer<AppSettings>(builder: (_, settings, __) {
        return MaterialApp(
          key: ValueKey('${settings.accentColorName}-${settings.appTheme}-${settings.appLanguage}'),
          title: 'Era',
          debugShowCheckedModeBanner: false,
          theme: _buildTheme(settings),
          locale: Locale(settings.appLanguage),
          builder: (_, child) => Directionality(
            textDirection: settings.appLanguage == 'ar'
                ? TextDirection.rtl : TextDirection.ltr,
            child: child!,
          ),
          home: const _SplashGate(),
        );
      }),
    );
  }

  ThemeData _buildTheme(AppSettings s) {
    final accent = utRed();
    final bg = appBg();
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: bg,
      colorScheme: ColorScheme.dark(
        primary: accent,
        secondary: accent,
        surface: bg,
        background: bg,
      ),
      fontFamily: 'ExpoArabic',
      appBarTheme: AppBarTheme(
        backgroundColor: bg,
        elevation: 0,
        titleTextStyle: TextStyle(
          fontFamily: 'ExpoArabic', fontSize: 20, fontWeight: FontWeight.w700, color: Colors.white),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: Colors.transparent,
        indicatorColor: accent.withOpacity(0.15),
        labelTextStyle: MaterialStateProperty.all(
          const TextStyle(fontFamily: 'ExpoArabic', fontSize: 11, color: Colors.white)),
      ),
      textTheme: const TextTheme(
        bodyLarge: TextStyle(fontFamily: 'ExpoArabic', color: Colors.white),
        bodyMedium: TextStyle(fontFamily: 'ExpoArabic', color: Colors.white70),
        titleMedium: TextStyle(fontFamily: 'ExpoArabic', fontWeight: FontWeight.w700, color: Colors.white),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: accent, foregroundColor: Colors.white,
          textStyle: const TextStyle(fontFamily: 'ExpoArabic', fontWeight: FontWeight.w700),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      ),
      sliderTheme: SliderThemeData(
        activeTrackColor: accent, thumbColor: accent,
        inactiveTrackColor: Colors.white24, trackHeight: 3,
      ),
      switchTheme: SwitchThemeData(
        thumbColor: MaterialStateProperty.resolveWith((s) => s.contains(MaterialState.selected) ? accent : null),
        trackColor: MaterialStateProperty.resolveWith((s) => s.contains(MaterialState.selected) ? accent.withOpacity(0.4) : null),
      ),
      progressIndicatorTheme: ProgressIndicatorThemeData(color: accent),
      popupMenuTheme: PopupMenuThemeData(
        color: const Color(0xFF1A1A1A), textStyle: const TextStyle(color: Colors.white)),
    );
  }
}

class _SplashGate extends StatefulWidget {
  const _SplashGate();
  @override State<_SplashGate> createState() => _SplashGateState();
}

class _SplashGateState extends State<_SplashGate> {
  bool _done = false;
  late final AppLinks _appLinks;

  @override void initState() {
    super.initState();
    _appLinks = AppLinks();
    _appLinks.uriLinkStream.listen(_handleDeepLink);
    _appLinks.getInitialLink().then((uri) { if (uri != null) _handleDeepLink(uri); });
    Future.delayed(const Duration(milliseconds: 1600), () {
      if (mounted) setState(() => _done = true);
    });
  }

  Future<void> _handleDeepLink(Uri uri) async {
    final fragment = uri.fragment.isNotEmpty ? uri.fragment : uri.query;
    final params = Uri.splitQueryString(fragment);
    final accessToken = params["access_token"];
    final refreshToken = params["refresh_token"] ?? "";
    if (accessToken == null || accessToken.isEmpty) return;
    try {
      final sm = SupabaseManager.instance;
      final info = await sm.getUserFromToken(accessToken);
      if (info == null) return;
      final meta = (info["user_metadata"] as Map<String, dynamic>?) ?? {};
      final user = SupabaseUser(
        id: info["id"] as String? ?? "",
        email: info["email"] as String?,
        userMetadata: meta,
        avatarUrl: meta["avatar_url"] as String? ?? "",
      );
      await AuthSession.instance.save(
        accessToken: accessToken, refreshToken: refreshToken, user: user,
      );
      // Sync all cloud data - same as email login
      final cloudFavs = await sm.fetchFavorites();
      if (cloudFavs.isNotEmpty) {
        // ignore: use_build_context_synchronously
        FavoritesStore.instance.mergeFromCloud(cloudFavs);
      }
      final cloudProg = await sm.fetchProgress();
      if (cloudProg.isNotEmpty) {
        WatchProgressStore.instance.mergeFromCloud(cloudProg);
      }
      final profile = await sm.fetchProfile();
      if (profile != null) {
        final av = profile["avatar_url"] as String? ?? "";
        if (av.isNotEmpty) await AuthSession.instance.updateAvatarUrl(av);
      }
      final isAdmin = await sm.fetchIsAdmin();
      AuthSession.instance.setAdmin(isAdmin);
      WatchlistStore.instance.fetchFromCloud();
    } catch (_) {}
  }

  @override Widget build(BuildContext context) {
    if (!_done) return const UTanLoader();
    return Directionality(
      textDirection: AppSettings.instance.appLanguage == 'ar'
          ? TextDirection.rtl : TextDirection.ltr,
      child: const MainTabScreen(),
    );
  }
}
""")

print("✅ main.dart + main_tab.dart written")

# --- android/app/src/main/AndroidManifest.xml patch helper -----------------
w("android/app/src/main/AndroidManifest.xml", r"""<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES"/>
    <uses-permission android:name="android.permission.READ_MEDIA_VIDEO"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.WAKE_LOCK"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        android:maxSdkVersion="28"/>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="32"/>

    <application
        android:label="Era"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:taskAffinity=""
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            <meta-data
              android:name="io.flutter.embedding.android.NormalTheme"
              android:resource="@style/NormalTheme"/>
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW"/>
                <category android:name="android.intent.category.DEFAULT"/>
                <category android:name="android.intent.category.BROWSABLE"/>
                <data android:scheme="utan"/>
            </intent-filter>
        </activity>
        <meta-data
            android:name="flutterEmbedding"
            android:value="2"/>
    </application>
    <queries>
        <intent>
            <action android:name="android.intent.action.VIEW"/>
            <category android:name="android.intent.category.BROWSABLE"/>
            <data android:scheme="https"/>
        </intent>
    </queries>
</manifest>
""")

# --- android/app/build.gradle -----------------------------------------------
w("android/app/build.gradle", r"""plugins {
    id "com.android.application"
    id "kotlin-android"
    id "dev.flutter.flutter-gradle-plugin"
}

def localProperties = new Properties()
def localPropertiesFile = rootProject.file('local.properties')
if (localPropertiesFile.exists()) {
    localPropertiesFile.withReader('UTF-8') { reader -> localProperties.load(reader) }
}

def flutterVersionCode = localProperties.getProperty('flutter.versionCode') ?: '1'
def flutterVersionName = localProperties.getProperty('flutter.versionName') ?: '1.0'

android {
    namespace "com.utan.flutter"
    compileSdk flutter.compileSdkVersion
    ndkVersion flutter.ndkVersion

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = '17'
    }

    sourceSets {
        main.java.srcDirs += 'src/main/kotlin'
    }

    defaultConfig {
        applicationId "com.utan.flutter"
        minSdkVersion 21
        targetSdkVersion flutter.targetSdkVersion
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
        multiDexEnabled true
    }

    buildTypes {
        release {
            signingConfig signingConfigs.debug
            minifyEnabled false
            shrinkResources false
        }
    }
}

flutter {
    source '../..'
}

dependencies {
    implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk7:$kotlin_version"
}
""")

# --- android/build.gradle ---------------------------------------------------
w("android/build.gradle", r"""allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.buildDir = '../build'
subprojects {
    project.buildDir = "${rootProject.buildDir}/${project.name}"
}
subprojects {
    project.evaluationDependsOn(':app')
}

tasks.register("clean", Delete) {
    delete rootProject.buildDir
}
""")

# --- android/settings.gradle ------------------------------------------------
w("android/settings.gradle", r"""pluginManagement {
    def flutterSdkPath = {
        def properties = new Properties()
        file("local.properties").withInputStream { properties.load(it) }
        def flutterSdkPath = properties.getProperty("flutter.sdk")
        assert flutterSdkPath != null, "flutter.sdk not set in local.properties"
        return flutterSdkPath
    }()

    includeBuild("${flutterSdkPath}/packages/flutter_tools/gradle")

    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

plugins {
    id "dev.flutter.flutter-gradle-plugin" version "1.0.0" apply false
}

include ":app"
""")

# --- android/gradle.properties ----------------------------------------------
w("android/gradle.properties", r"""org.gradle.jvmargs=-Xmx4G
android.useAndroidX=true
android.enableJetifier=true
""")

# --- android/app/src/main/kotlin/MainActivity.kt ----------------------------
os.makedirs(os.path.join(BASE, "android/app/src/main/kotlin/com/utan/flutter"), exist_ok=True)
w("android/app/src/main/kotlin/com/utan/flutter/MainActivity.kt", r"""package com.utan.flutter

import io.flutter.embedding.android.FlutterActivity

class MainActivity: FlutterActivity()
""")

print("✅ Android project files written")

# --- android res: styles, colors, drawables ---------------------------------
os.makedirs(os.path.join(BASE, "android/app/src/main/res/values"), exist_ok=True)
os.makedirs(os.path.join(BASE, "android/app/src/main/res/drawable"), exist_ok=True)
os.makedirs(os.path.join(BASE, "android/app/src/main/res/drawable-v21"), exist_ok=True)

w("android/app/src/main/res/values/styles.xml", r"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="LaunchTheme" parent="@android:style/Theme.Black.NoTitleBar">
        <item name="android:forceDarkAllowed">false</item>
        <item name="android:windowBackground">@drawable/launch_background</item>
    </style>
    <style name="NormalTheme" parent="@android:style/Theme.Black.NoTitleBar">
        <item name="android:forceDarkAllowed">false</item>
        <item name="android:windowBackground">?android:colorBackground</item>
    </style>
</resources>
""")

w("android/app/src/main/res/drawable/launch_background.xml", r"""<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@android:color/black"/>
</layer-list>
""")

w("android/app/src/main/res/drawable-v21/launch_background.xml", r"""<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@android:color/black"/>
</layer-list>
""")

# --- analysis_options.yaml --------------------------------------------------
w("analysis_options.yaml", r"""include: package:flutter_lints/flutter.yaml
linter:
  rules:
    avoid_print: false
    prefer_const_constructors: true
    use_key_in_widget_constructors: true
""")

# --- README.md ---------------------------------------------------------------
open(os.path.join(BASE, "..", "README.md"), "w", encoding="utf-8").write(r"""# UTan Flutter

Arabic/English video streaming app - Flutter port of the original Swift/SwiftUI application.

## Structure
```
UTan_Flutter/
+-- assets/
|   +-- fonts/     # Cairo, Rubik, IBMPlexArabic, ExpoArabic
|   +-- images/    # logo.png + category images
+-- lib/
    +-- main.dart
    +-- app_colors.dart
    +-- app_settings.dart
    +-- models/
    +-- services/
    +-- providers/
    +-- screens/
    +-- widgets/
    +-- player/
```

## Setup
```bash
cd UTan_Flutter
flutter pub get
flutter run
```

## Build APK
```bash
flutter build apk --release
```
""")

print("\n" + "-" * 60)
print("✅ DONE! Flutter project generated inside UTan_Flutter/")
print("-" * 60)
print("\nNext steps:")
print("  1. cd UTan_Flutter")
print("  2. flutter pub get")
print("  3. dart run flutter_launcher_icons   ← generates app icon from assets/images/app.jpg")
print("  4. flutter run     (or 'flutter build apk --release')")

# -- Auto-generate launcher icons if Pillow + app.jpg are available -----------
try:
    from PIL import Image
    src = os.path.join(BASE, 'assets', 'images', 'app.jpg')
    if os.path.exists(src):
        img = Image.open(src).convert('RGB')
        sizes = {
            'mipmap-mdpi':     48,
            'mipmap-hdpi':     72,
            'mipmap-xhdpi':    96,
            'mipmap-xxhdpi':  144,
            'mipmap-xxxhdpi': 192,
        }
        res_base = os.path.join(BASE, 'android', 'app', 'src', 'main', 'res')
        for folder, sz in sizes.items():
            d = os.path.join(res_base, folder)
            os.makedirs(d, exist_ok=True)
            resized = img.resize((sz, sz), Image.LANCZOS)
            resized.save(os.path.join(d, 'ic_launcher.png'))
            resized.save(os.path.join(d, 'ic_launcher_round.png'))
        print("✅ Launcher icons generated from assets/images/app.jpg")
    else:
        print("ℹ️  app.jpg not found yet - icons will be generated by 'dart run flutter_launcher_icons' after assets are copied")
except ImportError:
    print("ℹ️  Pillow not available - run: pip install Pillow  OR  dart run flutter_launcher_icons")
except Exception as e:
    print(f"⚠️  Icon generation skipped: {e}")
print("\nFonts + images must exist at:")
print("  UTan_Flutter/assets/fonts/")
print("  UTan_Flutter/assets/images/")
import os, sys

BASE = "UTan_Flutter"
DIRS = [
    f"{BASE}/lib/models",
    f"{BASE}/lib/services",
    f"{BASE}/lib/providers",
    f"{BASE}/lib/screens",
    f"{BASE}/lib/widgets",
    f"{BASE}/lib/player",
    f"{BASE}/assets/fonts",
    f"{BASE}/assets/images",
]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

def w(rel_path, content):
    full = os.path.join(BASE, rel_path) if not rel_path.startswith(".") else rel_path
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Directories created")

# --- pubspec.yaml ---
_pubspec = "name: utan_flutter\ndescription: UTan Video Streaming App\npublish_to: 'none'\nversion: 5.0.0+5\n\nenvironment:\n  sdk: '>=3.2.0 <4.0.0'\n  flutter: '>=3.22.0'\n\ndependencies:\n  flutter:\n    sdk: flutter\n  provider: ^6.1.2\n  http: ^1.2.1\n  cached_network_image: ^3.3.1\n  shared_preferences: ^2.3.0\n  video_player: ^2.8.6\n  chewie: ^1.8.1\n  intl: ^0.19.0\n  wakelock_plus: ^1.2.8\n  url_launcher: ^6.3.0\n  path_provider: ^2.1.4\n  flutter_cache_manager: ^3.4.1\n  supabase_flutter: ^2.5.3\n  google_sign_in: ^6.2.1\n  app_links: ^6.0.0\n  image_picker: ^1.0.7\n  webview_flutter: ^4.8.0\n  dio: ^5.4.3\n  rxdart: ^0.28.0\n\ndev_dependencies:\n  flutter_test:\n    sdk: flutter\n  flutter_lints: ^4.0.0\n  flutter_launcher_icons: ^0.14.1\n\nflutter_icons:\n  android: true\n  ios: false\n  image_path: 'assets/images/app.jpg'\n  adaptive_icon_background: '#0D0D0D'\n  adaptive_icon_foreground: 'assets/images/app.jpg'\n  min_sdk_android: 21\n\nflutter:\n  uses-material-design: true\n\n  assets:\n    - assets/images/\n\n  fonts:\n    - family: Cairo\n      fonts:\n        - asset: assets/fonts/Cairo.ttf\n          weight: 400\n        - asset: assets/fonts/Cairo-Bold-1.ttf\n          weight: 700\n    - family: Rubik\n      fonts:\n        - asset: assets/fonts/Rubik.ttf\n          weight: 400\n        - asset: assets/fonts/Rubik-Bold.ttf\n          weight: 700\n    - family: IBMPlexArabic\n      fonts:\n        - asset: assets/fonts/Ibm.ttf\n          weight: 400\n        - asset: assets/fonts/IBMPlexArabic-Bold.ttf\n          weight: 700\n    - family: ExpoArabic\n      fonts:\n        - asset: assets/fonts/alfont_com_AlFont_com_ExpoArabic-Bold.otf\n          weight: 700\n"
w("pubspec.yaml", _pubspec)
print("pubspec.yaml written")



# --- android res: styles, colors, drawables ---------------------------------
os.makedirs(os.path.join(BASE, "android/app/src/main/res/values"), exist_ok=True)
os.makedirs(os.path.join(BASE, "android/app/src/main/res/drawable"), exist_ok=True)
os.makedirs(os.path.join(BASE, "android/app/src/main/res/drawable-v21"), exist_ok=True)

w("android/app/src/main/res/values/styles.xml", r"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="LaunchTheme" parent="@android:style/Theme.Black.NoTitleBar">
        <item name="android:forceDarkAllowed">false</item>
        <item name="android:windowBackground">@drawable/launch_background</item>
    </style>
    <style name="NormalTheme" parent="@android:style/Theme.Black.NoTitleBar">
        <item name="android:forceDarkAllowed">false</item>
        <item name="android:windowBackground">?android:colorBackground</item>
    </style>
</resources>
""")

w("android/app/src/main/res/drawable/launch_background.xml", r"""<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@android:color/black"/>
</layer-list>
""")

w("android/app/src/main/res/drawable-v21/launch_background.xml", r"""<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@android:color/black"/>
</layer-list>
""")

# --- analysis_options.yaml --------------------------------------------------
w("analysis_options.yaml", r"""include: package:flutter_lints/flutter.yaml
linter:
  rules:
    avoid_print: false
    prefer_const_constructors: true
    use_key_in_widget_constructors: true
""")

# --- README.md ---------------------------------------------------------------
open(os.path.join(BASE, "..", "README.md"), "w", encoding="utf-8").write(r"""# UTan Flutter

Arabic/English video streaming app - Flutter port of the original Swift/SwiftUI application.

## Structure
```
UTan_Flutter/
+-- assets/
|   +-- fonts/     # Cairo, Rubik, IBMPlexArabic, ExpoArabic
|   +-- images/    # logo.png + category images
+-- lib/
    +-- main.dart
    +-- app_colors.dart
    +-- app_settings.dart
    +-- models/
    +-- services/
    +-- providers/
    +-- screens/
    +-- widgets/
    +-- player/
```

## Setup
```bash
cd UTan_Flutter
flutter pub get
flutter run
```

## Build APK
```bash
flutter build apk --release
```
""")

print("\n" + "-" * 60)
print("✅ DONE! Flutter project generated inside UTan_Flutter/")
print("-" * 60)
print("\nNext steps:")
print("  1. cd UTan_Flutter")
print("  2. flutter pub get")
print("  3. dart run flutter_launcher_icons   ← generates app icon from assets/images/app.jpg")
print("  4. flutter run     (or 'flutter build apk --release')")

# -- Auto-generate launcher icons if Pillow + app.jpg are available -----------
try:
    from PIL import Image
    src = os.path.join(BASE, 'assets', 'images', 'app.jpg')
    if os.path.exists(src):
        img = Image.open(src).convert('RGB')
        sizes = {
            'mipmap-mdpi':     48,
            'mipmap-hdpi':     72,
            'mipmap-xhdpi':    96,
            'mipmap-xxhdpi':  144,
            'mipmap-xxxhdpi': 192,
        }
        res_base = os.path.join(BASE, 'android', 'app', 'src', 'main', 'res')
        for folder, sz in sizes.items():
            d = os.path.join(res_base, folder)
            os.makedirs(d, exist_ok=True)
            resized = img.resize((sz, sz), Image.LANCZOS)
            resized.save(os.path.join(d, 'ic_launcher.png'))
            resized.save(os.path.join(d, 'ic_launcher_round.png'))
        print("✅ Launcher icons generated from assets/images/app.jpg")
    else:
        print("ℹ️  app.jpg not found yet - icons will be generated by 'dart run flutter_launcher_icons' after assets are copied")
except ImportError:
    print("ℹ️  Pillow not available - run: pip install Pillow  OR  dart run flutter_launcher_icons")
except Exception as e:
    print(f"⚠️  Icon generation skipped: {e}")
print("\nFonts + images must exist at:")
print("  UTan_Flutter/assets/fonts/")
print("  UTan_Flutter/assets/images/")
