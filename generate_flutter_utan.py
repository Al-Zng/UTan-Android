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
_pubspec = "name: utan_flutter\ndescription: UTan Video Streaming App\npublish_to: 'none'\nversion: 5.0.0+5\n\nenvironment:\n  sdk: '>=3.2.0 <4.0.0'\n  flutter: '>=3.22.0'\n\ndependencies:\n  flut[...]"
w("pubspec.yaml", _pubspec)
print("pubspec.yaml written")


# ─── lib/app_colors.dart ────────────────────────────────────────────────────
w("lib/app_colors.dart", r"""import 'package:flutter/material.dart';
import 'app_settings.dart';

// ─── Dynamic background based on selected theme ──────────────────────────
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

// ─── Dynamic accent color ─────────────────────────────────────────────────
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

// ─── L() localisation helper ─────────────────────────────────────────────
String L(String ar, String en) =>
    AppSettings.instance.appLanguage == 'en' ? en : ar;

// ─── App Font helper ─────────────────────────────────────────────────────
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
  switch (fontName.toLowerCase()) {
    case 'ibm':
      family = 'IBMPlexArabic';
      break;
    case 'rubik':
      family = 'Rubik';
      break;
    case 'cairo':
      family = 'Cairo';
      break;
    case 'expo':
      family = 'ExpoArabic';
      break;
    default:
      family = 'Cairo';
  }
  return TextStyle(
    fontFamily: family,
    fontSize: size,
    fontWeight: FontWeight.w700,
    color: color ?? Colors.white,
  );
}

// ─── Category color/icon helpers ─────────────────────────────────────────
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

// ─── Color from hex ───────────────────────────────────────────────────────
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

# ─── lib/services/scraper.dart ─────────────────────────────────────────────
# KEY FIX: Use proper regex escaping for raw strings with quotes
w("lib/services/scraper.dart", r"""import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../models/video_item.dart';
import '../models/media_details.dart';
import '../models/episode_item.dart';

// ────────────────────────────────────────────────────────────────
//  CONSTANTS
// ────────────────────────────────────────────────────────────────

/// Content metadata source (listing, search, details)
const String _ceeBase  = 'https://cee.buzz/api/android/';
const String _ceeCdn   = 'https://cnth2.cee.buzz/vascin-poster-images/';
const int    _ceeLevel = 1;

/// VidBox streaming source (video server resolution)
const String _vidboxBase = 'https://vidbox.dev';

/// Proxy fallback – append original URL after the '?url=' parameter
const String _proxyBase = 'https://proxy.kuro-pq9.workers.dev/?url=';

/// OpenSubtitles REST API v1
const String _osBase    = 'https://api.opensubtitles.com/api/v1';
const String _osApiKey  = 'srt7890uio12345';   // ← replace with your real key

// ────────────────────────────────────────────────────────────────
//  PROXY-AWARE HTTP HELPERS
// ────────────────────────────────────────────────────────────────

/// GET with automatic proxy fallback on any failure / timeout.
Future<http.Response?> _get(
  String url, {
  Map<String, String>? headers,
  Duration timeout = const Duration(seconds: 18),
}) async {
  // 1. Direct attempt
  try {
    final r = await http
        .get(Uri.parse(url), headers: headers)
        .timeout(timeout);
    if (r.statusCode < 500) return r;
  } catch (_) {}

  // 2. Proxy fallback
  try {
    final proxied = '$_proxyBase${Uri.encodeComponent(url)}';
    final r = await http
        .get(Uri.parse(proxied), headers: headers)
        .timeout(timeout);
    return r;
  } catch (_) {}

  return null;
}

// ────────────────────────────────────────────────────────────────
//  CEE.BUZZ HELPERS  (metadata only – unchanged logic)
// ────────────────────────────────────────────────────────────────

String _img(dynamic v) {
  if (v == null) return '';
  final s = v.toString().trim();
  if (s.isEmpty) return '';
  if (s.startsWith('http')) return s;
  return '$_ceeCdn$s';
}

String _str(dynamic v) => v?.toString().trim() ?? '';

dynamic _pick(Map<String, dynamic> m, List<String> keys) {
  for (final k in keys) { if (m.containsKey(k)) return m[k]; }
  return null;
}

VideoItem? _toItem(dynamic raw) {
  if (raw is! Map<String, dynamic>) return null;
  final id = _str(_pick(raw, ['id', 'videoId', 'video_id']));
  if (id.isEmpty) return null;
  final title  = _str(_pick(raw, ['title', 'titleAr', 'name', 'videoTitle']));
  final poster = _pick(raw, ['poster', 'posterImage', 'image', 'thumbnail', 'cover', 'banner']);
  final kind   = _str(_pick(raw, ['kind', 'videoKind', 'type']));
  final type   = (kind == '2' || kind == 'series') ? 'series' : 'movies';
  return VideoItem(id: id, title: title, imageUrl: _img(poster), type: type);
}

List<VideoItem> _toItems(dynamic raw) {
  if (raw is! List) return [];
  return raw.map(_toItem).whereType<VideoItem>().toList();
}

// ────────────────────────────────────────────────────────────────
//  VIDBOX STREAM RESOLUTION
// ────────────────────────────────────────────────────────────────

/// Holds one streaming server entry returned by VidBox.
class VidboxServer {
  final String name;
  final String embedUrl;
  VidboxServer({required this.name, required this.embedUrl});
}

/// Holds the resolved stream URLs for a single piece of content.
class VidboxResult {
  final String url;
  final String url720;
  final String url1080;
  final String url360;
  final String url4k;
  final List<VidboxServer> servers;

  const VidboxResult({
    this.url = '',
    this.url720 = '',
    this.url1080 = '',
    this.url360 = '',
    this.url4k = '',
    this.servers = const [],
  });
}

/// Fetch movie stream sources from VidBox.
/// [tmdbId] is the TMDB / VidBox content ID.
Future<VidboxResult> fetchVidboxMovie(String tmdbId) async {
  if (tmdbId.isEmpty) return const VidboxResult();

  // ── Try the VidBox JSON API first ──────────────────────────────────────
  final apiUrl = '$_vidboxBase/api/movie?id=$tmdbId';
  final apiResp = await _get(apiUrl, headers: {
    'Referer': '$_vidboxBase/',
    'Origin' : _vidboxBase,
    'Accept' : 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36',
  });

  if (apiResp != null && apiResp.statusCode == 200) {
    final result = _parseVidboxApiResponse(apiResp.body);
    if (result.url.isNotEmpty || result.servers.isNotEmpty) return result;
  }

  // ── Fallback: scrape the embed page ────────────────────────────────────
  final embedUrl = '$_vidboxBase/embed/movie/$tmdbId';
  return _scrapeVidboxEmbedPage(embedUrl);
}

/// Fetch TV episode stream sources from VidBox.
Future<VidboxResult> fetchVidboxEpisode(
    String tmdbId, int season, int episode) async {
  if (tmdbId.isEmpty) return const VidboxResult();

  // ── Try the VidBox JSON API first ──────────────────────────────────────
  final apiUrl =
      '$_vidboxBase/api/episodes?id=$tmdbId&s=$season&e=$episode';
  final apiResp = await _get(apiUrl, headers: {
    'Referer': '$_vidboxBase/',
    'Origin' : _vidboxBase,
    'Accept' : 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36',
  });

  if (apiResp != null && apiResp.statusCode == 200) {
    final result = _parseVidboxApiResponse(apiResp.body);
    if (result.url.isNotEmpty || result.servers.isNotEmpty) return result;
  }

  // ── Fallback: scrape embed page ─────────────────────────────────────────
  final embedUrl = '$_vidboxBase/embed/tv/$tmdbId/$season/$episode';
  return _scrapeVidboxEmbedPage(embedUrl);
}

/// Parse JSON API response from VidBox into a [VidboxResult].
VidboxResult _parseVidboxApiResponse(String body) {
  try {
    final dynamic json = jsonDecode(body);
    if (json is! Map<String, dynamic>) return const VidboxResult();

    // Extract sources array
    final dynamic rawSources =
        json['sources'] ?? json['streams'] ?? json['data'];
    final List<dynamic> sourceList =
        rawSources is List ? rawSources : <dynamic>[];

    // Extract server list (embed iframes)
    final dynamic rawServers =
        json['servers'] ?? json['embeds'] ?? json['players'];
    final List<dynamic> serverList =
        rawServers is List ? rawServers : <dynamic>[];

    final servers = serverList
        .whereType<Map>()
        .map((s) {
          final sm = Map<String, dynamic>.from(s);
          return VidboxServer(
            name:     _str(_pick(sm, ['name', 'server', 'title', 'provider'])),
            embedUrl: _str(_pick(sm, ['url', 'embed', 'link', 'embedUrl', 'src'])),
          );
        })
        .where((s) => s.embedUrl.isNotEmpty)
        .toList();

    // Pick best direct URL from sources
    final result = _pickBestSourceUrls(sourceList);

    return VidboxResult(
      url:     result['auto']  ?? '',
      url720:  result['720']   ?? '',
      url1080: result['1080']  ?? '',
      url360:  result['360']   ?? '',
      url4k:   result['4k']    ?? '',
      servers: servers,
    );
  } catch (_) {
    return const VidboxResult();
  }
}

/// Pick the best direct-stream URL per quality level from a sources list.
Map<String, String> _pickBestSourceUrls(List<dynamic> sources) {
  String q360 = '', q480 = '', q720 = '', q1080 = '', q4k = '', first = '';
  for (final s in sources) {
    if (s is! Map) continue;
    final sm = Map<String, dynamic>.from(s);
    final url = _str(_pick(sm, ['url', 'file', 'src', 'link', 'path']));
    if (url.isEmpty) continue;
    if (first.isEmpty) first = url;
    final q = _str(_pick(sm, ['quality', 'resolution', 'label', 'size'])).toLowerCase();
    if (q.contains('4k') || q.contains('2160'))      q4k   = url;
    else if (q.contains('1080'))                      q1080 = url;
    else if (q.contains('720'))                       q720  = url;
    else if (q.contains('480'))                       q480  = url;
    else if (q.contains('360'))                       q360  = url;
  }
  final auto = q720.isNotEmpty  ? q720
             : q480.isNotEmpty  ? q480
             : q360.isNotEmpty  ? q360
             : q1080.isNotEmpty ? q1080
             : first;
  return {
    'auto': auto,
    '720' : q720,
    '1080': q1080,
    '360' : q360,
    '4k'  : q4k,
  };
}

/// Scrape the VidBox embed page HTML to extract stream sources.
Future<VidboxResult> _scrapeVidboxEmbedPage(String embedUrl) async {
  final resp = await _get(embedUrl, headers: {
    'Referer'   : '$_vidboxBase/',
    'Origin'    : _vidboxBase,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36',
  });
  if (resp == null || resp.statusCode != 200) return const VidboxResult();

  final html = utf8.decode(resp.bodyBytes);

  // Pattern 1 – window.__NUXT__ / window.app JSON blob
  final jsonBlobs = RegExp(r'(?:window\.__(?:NUXT|APP|DATA)__|var\s+(?:sources|streams|data)\s*=)\s*(\{.+?\});', dotAll: true)
      .allMatches(html)
      .map((m) => m.group(1) ?? '')
      .where((s) => s.isNotEmpty);

  for (final blob in jsonBlobs) {
    try {
      final dynamic parsed = jsonDecode(blob);
      if (parsed is Map<String, dynamic>) {
        final result = _parseVidboxApiResponse(jsonEncode(parsed));
        if (result.url.isNotEmpty || result.servers.isNotEmpty) return result;
      }
    } catch (_) {}
  }

  // Pattern 2 – <script type="application/json"> blocks
  // FIX: Use escaped quotes in raw string or switch to regular string
  final scriptJsons = RegExp(r'<script[^>]*type=["\x27]application/json["\x27][^>]*>(.*?)</script>', dotAll: true)
      .allMatches(html)
      .map((m) => m.group(1)?.trim() ?? '');

  for (final blob in scriptJsons) {
    if (blob.isEmpty) continue;
    try {
      final dynamic parsed = jsonDecode(blob);
      if (parsed is Map<String, dynamic>) {
        final result = _parseVidboxApiResponse(jsonEncode(parsed));
        if (result.url.isNotEmpty || result.servers.isNotEmpty) return result;
      }
    } catch (_) {}
  }

  // Pattern 3 – look for inline source arrays like:  sources:[{file:"...",label:"720"}]
  final inlineSourcesMatch = RegExp(r'sources\s*:\s*(\[.+?\])', dotAll: true)
      .firstMatch(html);
  if (inlineSourcesMatch != null) {
    try {
      final dynamic arr = jsonDecode(inlineSourcesMatch.group(1)!);
      if (arr is List) {
        final picked = _pickBestSourceUrls(arr);
        if (picked['auto']?.isNotEmpty == true) {
          return VidboxResult(
            url:     picked['auto']  ?? '',
            url720:  picked['720']   ?? '',
            url1080: picked['1080']  ?? '',
            url360:  picked['360']   ?? '',
            url4k:   picked['4k']    ?? '',
          );
        }
      }
    } catch (_) {}
  }

  // Pattern 4 – collect iframe src attributes as server list
  // FIX: Use hex escape for quotes
  final iframeSrcs = RegExp(r'<iframe[^>]+src=["\x27]([^\x22\x27]+)["\x27]', caseSensitive: false)
      .allMatches(html)
      .map((m) => m.group(1) ?? '')
      .where((u) => u.startsWith('http'))
      .toList();

  if (iframeSrcs.isNotEmpty) {
    final servers = iframeSrcs
        .asMap()
        .entries
        .map((e) => VidboxServer(name: 'Server ${e.key + 1}', embedUrl: e.value))
        .toList();
    return VidboxResult(servers: servers);
  }

  return const VidboxResult();
}

// ───────────────────────────────────────────────────────────────
//  OPENSUBTITLES ARABIC SUBTITLES
// ───────────────────────────────────────────────────────────────

/// Fetch the best Arabic subtitle URL for a movie given its IMDb ID.
/// Returns a .vtt or .srt URL, or empty string on failure.
Future<String> fetchArabicSubtitle(
  String imdbId, {
  int? seasonNumber,
  int? episodeNumber,
}) async {
  if (imdbId.isEmpty) return '';

  // Clean IMDb ID to numeric-only part expected by OS API (e.g. "0213338")
  final numericId = imdbId.replaceAll(RegExp(r'[^0-9]'), '');
  if (numericId.isEmpty) return '';

  final params = <String, String>{
    'imdb_id'  : numericId,
    'languages': 'ar',
    'order_by' : 'download_count',
  };
  if (seasonNumber  != null) params['season_number']  = '$seasonNumber';
  if (episodeNumber != null) params['episode_number'] = '$episodeNumber';

  final searchUrl =
      '$_osBase/subtitles?${params.entries.map((e) => '${e.key}=${Uri.encodeComponent(e.value)}').join('&')}';

  final resp = await _get(searchUrl, headers: {
    'Api-Key'   : _osApiKey,
    'Content-Type': 'application/json',
    'User-Agent': 'UTanApp v1.0',
  });

  if (resp == null || resp.statusCode != 200) return '';

  try {
    final json = jsonDecode(utf8.decode(resp.bodyBytes)) as Map<String, dynamic>;
    final data = json['data'];
    if (data is! List || data.isEmpty) return '';

    // Pick the first subtitle entry
    final entry = data.first as Map<String, dynamic>;
    final attrs  = entry['attributes'] as Map<String, dynamic>?;
    if (attrs == null) return '';

    final files = attrs['files'] as List<dynamic>?;
    if (files == null || files.isEmpty) return '';

    final fileId = (files.first as Map<String, dynamic>)['file_id'];
    if (fileId == null) return '';

    // Download link request
    return await _openSubtitlesDownloadUrl(fileId.toString());
  } catch (_) {}
  return '';
}

/// Request a direct download URL from the OpenSubtitles /download endpoint.
Future<String> _openSubtitlesDownloadUrl(String fileId) async {
  const downloadUrl = '$_osBase/download';
  try {
    final body = jsonEncode({'file_id': int.parse(fileId), 'sub_format': 'vtt'});
    http.Response? resp;

    // Direct attempt
    try {
      resp = await http.post(
        Uri.parse(downloadUrl),
        headers: {
          'Api-Key'     : _osApiKey,
          'Content-Type': 'application/json',
          'User-Agent'  : 'UTanApp v1.0',
        },
        body: body,
      ).timeout(const Duration(seconds: 15));
    } catch (_) {}

    // Proxy fallback
    if (resp == null || resp.statusCode != 200) {
      try {
        resp = await http.post(
          Uri.parse('$_proxyBase${Uri.encodeComponent(downloadUrl)}'),
          headers: {
            'Api-Key'     : _osApiKey,
            'Content-Type': 'application/json',
            'User-Agent'  : 'UTanApp v1.0',
          },
          body: body,
        ).timeout(const Duration(seconds: 18));
      } catch (_) {}
    }

    if (resp != null && resp.statusCode == 200) {
      final json = jsonDecode(utf8.decode(resp.bodyBytes)) as Map<String, dynamic>;
      final link = json['link'] as String?;
      if (link != null && link.isNotEmpty) return link;
    }
  } catch (_) {}
  return '';
}

// ───────────────────────────────────────────────────────────────
//  CEE.BUZZ METADATA HELPERS  (unchanged from original)
// ───────────────────────────────────────────────────────────────

Future<List<dynamic>> _getCeeFiles(String id) async {
  try {
    final r = await _get('${_ceeBase}transcoddedFiles/id/$id');
    if (r != null && r.statusCode == 200) {
      final body = jsonDecode(utf8.decode(r.bodyBytes));
      if (body is List) return body;
      if (body is Map) {
        return (body['files'] ?? body['data'] ?? body['streams'] ?? []) as List;
      }
    }
  } catch (_) {}
  return [];
}

String _ceeBestUrl(List<dynamic> files, {String prefer = ''}) {
  if (files.isEmpty) return '';
  String q360 = '', q480 = '', q720 = '', q1080 = '', q4k = '', first = '';
  for (final f in files) {
    if (f is! Map<String, dynamic>) continue;
    final url = _str(_pick(f, ['url', 'file', 'src', 'path', 'link']));
    if (url.isEmpty) continue;
    if (first.isEmpty) first = url;
    final q = _str(_pick(f, ['quality', 'resolution', 'label'])).toLowerCase();
    if (q.contains('4k') || q.contains('2160')) q4k   = url;
    else if (q.contains('1080'))                q1080 = url;
    else if (q.contains('720'))                 q720  = url;
    else if (q.contains('480'))                 q480  = url;
    else if (q.contains('360'))                 q360  = url;
  }
  if (prefer == '1080' && q1080.isNotEmpty) return q1080;
  if (prefer == '720'  && q720.isNotEmpty)  return q720;
  if (prefer == '360'  && q360.isNotEmpty)  return q360;
  if (prefer == '4k'   && q4k.isNotEmpty)   return q4k;
  return q720.isNotEmpty ? q720 : (q480.isNotEmpty ? q480 : (q360.isNotEmpty ? q360 : (q1080.isNotEmpty ? q1080 : first)));
}

// ───────────────────────────────────────────────────────────────
//  MOVIE SCRAPER  (home / search / category – metadata from cee.buzz)
// ───────────────────────────────────────────────────────────────

class MovieScraper extends ChangeNotifier {
  List<VideoItem> heroItems = [];
  List<({String name, List<VideoItem> items, int tagId})> categories = [];
  List<VideoItem> allItemsPool = [];
  List<({int id, String nameAr, String nameEn})> dynamicCategories = [];
  bool isLoading = false;

  Future<void> fetchHome() async {
    isLoading = true;
    notifyListeners();
    try {
      await _fetchDynamicCategories();

      final bannerResp = await _get(
        '${_ceeBase}banner/level/$_ceeLevel',
      );
      if (bannerResp != null && bannerResp.statusCode == 200) {
        final bd = jsonDecode(utf8.decode(bannerResp.bodyBytes));
        final list = bd is List
            ? bd
            : (bd is Map ? (bd['data'] ?? bd['items'] ?? bd['videos'] ?? []) : []);
        heroItems = _toItems(list);
      }

      final groupResp = await _get(
        '${_ceeBase}videoGroups/lang/ar/level/$_ceeLevel',
      );
      if (groupResp != null && groupResp.statusCode == 200) {
        final gd = jsonDecode(utf8.decode(groupResp.bodyBytes));
        final groups = gd is List
            ? gd
            : (gd is Map ? (gd['data'] ?? gd['groups'] ?? []) : []) as List;
        final secs = <({String name, List<VideoItem> items, int tagId})>[];
        for (final g in groups) {
          if (g is! Map<String, dynamic>) continue;
          final name = _str(_pick(g, ['title', 'titleAr', 'name', 'groupTitle']));
          final gid  = int.tryParse(_str(_pick(g, ['id', 'groupId', 'groupID']))) ?? -1;
          final raw  = _pick(g, ['videos', 'items', 'data', 'results']);
          final items = _toItems(raw);
          if (name.isNotEmpty && items.isNotEmpty) {
            secs.add((name: name, items: items, tagId: gid));
            if (heroItems.isEmpty && items.length >= 4) {
              heroItems = items.take(8).toList();
            }
          }
        }
        categories = secs;
        allItemsPool = secs.expand((s) => s.items).toList();
      }

      if (heroItems.isEmpty) {
        final lr = await _get(
          '${_ceeBase}latestMovies/level/$_ceeLevel/itemsPerPage/8/page/1/',
        );
        if (lr != null && lr.statusCode == 200) {
          final ld = jsonDecode(utf8.decode(lr.bodyBytes));
          heroItems = _toItems(
              ld is List ? ld : (ld is Map ? (ld['data'] ?? ld['items'] ?? []) : []));
        }
      }
    } catch (_) {}
    isLoading = false;
    notifyListeners();
  }

  Future<void> refreshHome() async => fetchHome();

  Future<void> _fetchDynamicCategories() async {
    try {
      final r = await _get('${_ceeBase}mainCategories?lang=ar');
      if (r != null && r.statusCode == 200) {
        final raw = jsonDecode(utf8.decode(r.bodyBytes));
        final list = raw is List
            ? raw
            : (raw is Map
                ? (raw['data'] ?? raw['categories'] ?? raw['items'] ?? [])
                : []) as List;
        dynamicCategories = list
            .whereType<Map>()
            .map((m) {
              final mm = Map<String, dynamic>.from(m);
              return (
                id: int.tryParse(_str(_pick(mm, ['id', 'categoryId', 'category_id']))) ?? 0,
                nameAr: _str(_pick(mm, ['nameAr', 'name', 'titleAr', 'title', 'nameArabe'])),
                nameEn: _str(_pick(mm, ['nameEn', 'nameEnglish', 'titleEn'])),
              );
            })
            .where((c) => c.id > 0 && c.nameAr.isNotEmpty)
            .toList();
        notifyListeners();
      }
    } catch (_) {}
  }

  Future<List<VideoItem>> fetchCategory(
    int typeId, {
    int page = 1,
    bool useTag = false,
    String sort = 'date',
    String? genre,
  }) async {
    try {
      Uri uri;
      if (useTag) {
        uri = Uri.parse(
          '${_ceeBase}video/V/2/itemsPerPage/30/level/$_ceeLevel'
          '/videoKind/$typeId/sortParam/$sort/pageNumber/${page - 1}',
        );
      } else {
        uri = Uri.parse(
          '${_ceeBase}videosByCategory?categoryID=$typeId'
          '&orderby=$sort&videoKind=0&offset=${(page - 1) * 30}&level=$_ceeLevel',
        );
      }
      final r = await _get(uri.toString());
      if (r != null && r.statusCode == 200) {
        final body = jsonDecode(utf8.decode(r.bodyBytes));
        final items = body is List
            ? body
            : (body is Map
                ? (body['data'] ?? body['items'] ?? body['videos'] ?? [])
                : []);
        return _toItems(items);
      }
    } catch (_) {}
    return [];
  }

  Future<bool> hasMorePages(String html, int currentPage) async => true;

  Future<List<VideoItem>> advancedSearch({
    String? title,
    String? genre,
    String? type,
    String? year,
    String? language,
    String? director,
    String? imdbrate,
  }) async {
    if (title == null || title.isEmpty) return [];
    return searchItems(title);
  }

  Future<List<VideoItem>> searchItems(String query) async {
    if (query.trim().isEmpty) return [];
    try {
      final encoded = Uri.encodeComponent(query.trim());
      final r = await _get(
        '${_ceeBase}video/V/2/itemsPerPage/20/video_title_search/$encoded'
        '/itemsPerPage/12/pageNumber/0/level/$_ceeLevel',
      );
      if (r != null && r.statusCode == 200) {
        final body = jsonDecode(utf8.decode(r.bodyBytes));
        final items = body is List
            ? body
            : (body is Map
                ? (body['data'] ?? body['items'] ?? body['videos'] ??
                    body['results'] ?? [])
                : []);
        return _toItems(items);
      }
    } catch (_) {}
    return [];
  }

  // ── Full detail fetch: metadata from cee.buzz + streams from VidBox ──────

  Future<MediaDetails> fetchDetails(String id) async {
    final d = MediaDetails();
    try {
      // ── 1. Metadata from cee.buzz ────────────────────────────────────────
      final infoResp = await _get('${_ceeBase}allVideoInfo/id/$id');
      if (infoResp == null || infoResp.statusCode != 200) return d;

      final info = jsonDecode(utf8.decode(infoResp.bodyBytes));
      final Map<String, dynamic> m = info is Map<String, dynamic>
          ? info
          : (info is List && info.isNotEmpty
              ? info.first as Map<String, dynamic>
              : {});

      d.title    = _str(_pick(m, ['title', 'titleAr', 'videoTitle', 'name']));
      d.synopsis = _str(_pick(m, ['description', 'synopsis', 'overview', 'plot', 'story']));
      d.year     = _str(_pick(m, ['year', 'releaseYear', 'productionYear']));
      d.rating   = _str(_pick(m, ['imdbRating', 'rating', 'imdb', 'score']));
      d.runtime  = _str(_pick(m, ['runtime', 'duration', 'movieRuntime']));

      final poster = _pick(m, ['poster', 'posterImage', 'image', 'cover', 'thumbnail', 'banner']);
      d.imageUrl = _img(poster);

      final genreRaw = _pick(m, ['genres', 'categories', 'genre', 'tags']);
      if (genreRaw is List) {
        d.genre = genreRaw.map((g) {
          if (g is Map) {
            return _str(_pick(g as Map<String, dynamic>, ['name', 'nameAr', 'title']));
          }
          return g.toString();
        }).where((s) => s.isNotEmpty).join(' | ');
      } else {
        d.genre = _str(genreRaw);
      }

      // Extract IMDb ID for subtitle lookup
      final imdbId = _str(_pick(m, ['imdb', 'imdbId', 'imdb_id', 'imdbCode', 'tt']));
      // Extract TMDB ID (VidBox uses TMDB IDs)
      final tmdbId = _str(_pick(m, ['tmdbId', 'tmdb_id', 'tmdb', 'externalId']));
      // VidBox ID: prefer tmdbId, fall back to cee id
      final vidboxId = tmdbId.isNotEmpty ? tmdbId : id;

      final kind     = _str(_pick(m, ['kind', 'videoKind', 'type']));
      final isSeries = kind == '2' || kind == 'series';

      if (!isSeries) {
        // ── Movie ────────────────────────────────────────────────────────
        d.isMovie = true;

        // Fetch streams from VidBox (with proxy fallback built-in)
        final vidboxResult = await fetchVidboxMovie(vidboxId);

        if (vidboxResult.url.isNotEmpty) {
          d.movieUrl     = vidboxResult.url;
          d.movieUrl720  = vidboxResult.url720;
          d.movieUrl1080 = vidboxResult.url1080;
          d.movieUrl360  = vidboxResult.url360;
          d.movieUrl4k   = vidboxResult.url4k;
        } else {
          // Fallback to cee.buzz direct files if VidBox returns nothing
          final files = await _getCeeFiles(id);
          d.movieUrl     = _ceeBestUrl(files);
          d.movieUrl720  = _ceeBestUrl(files, prefer: '720');
          d.movieUrl1080 = _ceeBestUrl(files, prefer: '1080');
          d.movieUrl360  = _ceeBestUrl(files, prefer: '360');
          d.movieUrl4k   = _ceeBestUrl(files, prefer: '4k');
        }

        // ── Arabic subtitle via OpenSubtitles ───────────────────────────
        if (imdbId.isNotEmpty) {
          d.movieSubtitleVttUrl = await fetchArabicSubtitle(imdbId);
        }

      } else {
        // ── Series ──────────────────────────────────────────────────────
        d.isMovie = false;

        final seasResp = await _get('${_ceeBase}videoSeason/id/$id');
        List<dynamic> seasons = [];
        if (seasResp != null && seasResp.statusCode == 200) {
          final sd = jsonDecode(utf8.decode(seasResp.bodyBytes));
          seasons = sd is List
              ? sd
              : (sd is Map ? (sd['data'] ?? sd['seasons'] ?? []) : []) as List;
        }

        String _seasonLabel(dynamic s) {
          if (s is! Map<String, dynamic>) return '';
          return _str(_pick(s, ['name', 'title', 'seasonName', 'nameAr']));
        }

        // Parse season numbers for VidBox requests
        int _parseSeason(dynamic s) {
          if (s is! Map<String, dynamic>) return 1;
          final num = _str(_pick(s, ['seasonNumber', 'number', 'num', 'season']));
          return int.tryParse(num) ?? 1;
        }

        final limitedSeasons = seasons.take(6).toList();
        final seasonEpFutures = limitedSeasons.map((season) async {
          if (season is! Map<String, dynamic>) return <EpisodeItem>[];
          final sid    = _str(_pick(season, ['id', 'seasonId', 'season_id']));
          if (sid.isEmpty) return <EpisodeItem>[];
          final sLabel  = _seasonLabel(season);
          final sNumber = _parseSeason(season);

          try {
            final epResp = await _get('${_ceeBase}videoSeasonNumber/id/$sid');
            if (epResp == null || epResp.statusCode != 200) return <EpisodeItem>[];
            final ed = jsonDecode(utf8.decode(epResp.bodyBytes));
            final epList = ed is List
                ? ed
                : (ed is Map ? (ed['data'] ?? ed['episodes'] ?? []) : []);

            final limitedEps = (epList as List).take(24).toList();
            final epFutures = limitedEps.asMap().entries.map((entry) async {
              final epIndex = entry.key;
              final ep      = entry.value;
              if (ep is! Map<String, dynamic>) return null;

              final epId  = _str(_pick(ep, ['id', 'episodeId', 'episode_id']));
              if (epId.isEmpty) return null;
              final epNumStr = _str(_pick(ep, ['episodeNumber', 'episode', 'number', 'ep']));
              final epNumber = int.tryParse(epNumStr) ?? (epIndex + 1);
              var   epTitle  = _str(_pick(ep, ['title', 'titleAr', 'name', 'episodeTitle']));
              if (epTitle.isEmpty) epTitle = '$sLabel الحلقة $epNumber';
              final epPoster = _pick(ep, ['poster', 'thumbnail', 'image', 'cover']);

              // ── Stream URLs from VidBox ──────────────────────────────
              VidboxResult vidResult = await fetchVidboxEpisode(
                vidboxId, sNumber, epNumber,
              );

              String epUrl     = vidResult.url;
              String epUrl720  = vidResult.url720;
              String epUrl1080 = vidResult.url1080;
              String epUrl360  = vidResult.url360;
              String epUrl4k   = vidResult.url4k;

              // Fallback to cee.buzz episode files
              if (epUrl.isEmpty) {
                final embedded = _pick(ep, ['transcoddedFiles', 'files', 'streams', 'qualities']);
                List<dynamic> files = [];
                if (embedded is List && embedded.isNotEmpty) {
                  files = embedded;
                } else {
                  files = await _getCeeFiles(epId);
                }
                epUrl     = _ceeBestUrl(files);
                epUrl720  = _ceeBestUrl(files, prefer: '720');
                epUrl1080 = _ceeBestUrl(files, prefer: '1080');
                epUrl360  = _ceeBestUrl(files, prefer: '360');
                epUrl4k   = _ceeBestUrl(files, prefer: '4k');
              }

              // ── Arabic subtitle via OpenSubtitles ────────────────────
              String subUrl = '';
              if (imdbId.isNotEmpty) {
                subUrl = await fetchArabicSubtitle(
                  imdbId,
                  seasonNumber:  sNumber,
                  episodeNumber: epNumber,
                );
              }

              return EpisodeItem(
                id:     epId,
                title:  epTitle,
                season: sLabel,
                url:     epUrl,
                url720:  epUrl720,
                url1080: epUrl1080,
                url360:  epUrl360,
                url4k:   epUrl4k,
                subtitleVttUrl: subUrl,
                imageUrl: _img(epPoster),
              );
            });

            final results = await Future.wait(epFutures);
            return results.whereType<EpisodeItem>().toList();
          } catch (_) {
            return <EpisodeItem>[];
          }
        });

        final allSeasonEps = await Future.wait(seasonEpFutures);
        for (final eps in allSeasonEps) {
          d.episodes.addAll(eps);
        }
      }
    } catch (_) {}
    return d;
  }
}
""")

print("✅ scraper.dart written with FIXED regex patterns")

print("\n✅ DONE! Fixed Flutter scraper.dart")
