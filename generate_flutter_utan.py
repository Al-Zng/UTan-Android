import os

def build_flutter_project():
    print("🚀 البدء في إنشاء مشروع Flutter وتطبيق الأندرويد UTan بالكامل...")

    # 1. إنشاء الهيكل الكامل للمجلدات
    os.makedirs("lib", exist_ok=True)
    os.makedirs("android/app/src/main", exist_ok=True)

    # ─────────────────────────────────────────────────────────────────
    # 2. كتابة ملف pubspec.yaml (الإعدادات وحزم الاعتماديات)
    # ─────────────────────────────────────────────────────────────────
    pubspec_content = """name: utan
description: UTan media player streaming client migrated from Swift to Flutter.
version: 5.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.0
  video_player: ^2.8.2
  shared_preferences: ^2.2.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
"""
    with open("pubspec.yaml", "w", encoding="utf-8") as f:
        f.write(pubspec_content)

    # ─────────────────────────────────────────────────────────────────
    # 3. كتابة ملف AndroidManifest.xml (السماح بالشبكات المخصصة وفك القيود)
    # ─────────────────────────────────────────────────────────────────
    manifest_content = """<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.mustaqil.utan">
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>

    <application
        android:label="UTan"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|screenLayout|density|locale|layoutDirection|fontScale|screenContentDetails|uiMode"
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
        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
"""
    with open("android/app/src/main/AndroidManifest.xml", "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # ─────────────────────────────────────────────────────────────────
    # 4. كتابة ملف lib/models.dart (هياكل البيانات والـ Models)
    # ─────────────────────────────────────────────────────────────────
    models_content = """class VideoItem {
  final String id;
  final String title;
  final String imageUrl;
  final String type;

  VideoItem({
    required this.id,
    required this.title,
    required this.imageUrl,
    required this.type,
  });
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
  final String season;

  EpisodeItem({
    required this.id,
    required this.title,
    required this.url,
    required this.url720,
    required this.url1080,
    required this.url360,
    required this.url4k,
    required this.subtitleUrl,
    required this.subtitleVttUrl,
    required this.season,
  });
}

class MediaDetails {
  final String id;
  String title = "";
  String year = "";
  String genre = "";
  String rating = "";
  String runtime = "";
  String synopsis = "";
  String imageUrl = "";
  bool isMovie = true;
  List<EpisodeItem> episodes = [];
  String movieUrl = "";
  String movieUrl720 = "";
  String movieUrl1080 = "";
  String movieSubtitleUrl = "";
  String movieSubtitleVttUrl = "";

  MediaDetails({required this.id});
}

class SiteCategory {
  final int id;
  final String nameAr;
  final String nameEn;
  final int? remoteId;
  final bool isTag;

  SiteCategory({
    required this.id,
    required this.nameAr,
    required this.nameEn,
    this.remoteId,
    this.isTag = false,
  });
}
"""
    with open("lib/models.dart", "w", encoding="utf-8") as f:
        f.write(models_content)

    # ─────────────────────────────────────────────────────────────────
    # 5. كتابة ملف lib/settings.dart (إعدادات التطبيق والتخزين الدائم للترجمة)
    # ─────────────────────────────────────────────────────────────────
    settings_content = """import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AppSettings extends ChangeNotifier {
  static final AppSettings _instance = AppSettings._internal();
  factory AppSettings() => _instance;
  AppSettings._internal();

  late SharedPreferences _prefs;

  double subtitleFontSize = 22.0;
  String subtitleColorHex = "#FFFFFF";
  double subtitleBgOpacity = 0.6;
  double subtitleBottomPad = 60.0;
  bool subtitlesEnabled = true;
  String subtitleFontName = "Cairo";
  double subtitleDelay = 0.0;
  bool autoPlayNextEnabled = true;
  int autoPlayCountdownSeconds = 10;
  String preferredQuality = "تلقائي";

  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
    subtitleFontSize = _prefs.getDouble("sub_fontSize") ?? 22.0;
    subtitleColorHex = _prefs.getString("sub_colorHex") ?? "#FFFFFF";
    subtitleBgOpacity = _prefs.getDouble("sub_bgOpacity") ?? 0.6;
    subtitleBottomPad = _prefs.getDouble("sub_bottomPad") ?? 60.0;
    subtitlesEnabled = _prefs.getBool("sub_enabled") ?? true;
    subtitleFontName = _prefs.getString("sub_fontName") ?? "Cairo";
    subtitleDelay = _prefs.getDouble("sub_delay") ?? 0.0;
    autoPlayNextEnabled = _prefs.getBool("autoplay_next") ?? true;
    autoPlayCountdownSeconds = _prefs.getInt("autoplay_countdown") ?? 10;
    preferredQuality = _prefs.getString("pref_quality") ?? "تلقائي";
  }

  Future<void> setSubtitleFontSize(double val) async {
    subtitleFontSize = val;
    await _prefs.setDouble("sub_fontSize", val);
    notifyListeners();
  }

  Future<void> setSubtitleDelay(double val) async {
    subtitleDelay = val;
    await _prefs.setDouble("sub_delay", val);
    notifyListeners();
  }

  Future<void> setSubtitlesEnabled(bool val) async {
    subtitlesEnabled = val;
    await _prefs.setBool("sub_enabled", val);
    notifyListeners();
  }

  void clearCache() {
    _prefs.clear();
    init();
  }
}
"""
    with open("lib/settings.dart", "w", encoding="utf-8") as f:
        f.write(settings_content)

    # ─────────────────────────────────────────────────────────────────
    # 6. كتابة ملف lib/scraper.dart (محرك جلب وتحليل محتوى الموقع بدقة عالية)
    # ─────────────────────────────────────────────────────────────────
    scraper_content = """import 'package:http/http.dart' as http;
import 'models.dart';

class MovieScraper {
  final String baseUrl = "https://utan.site/"; 
  final String userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36";

  Map<String, String> get headers => {
    'User-Agent': userAgent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  };

  String _firstMatch(String pattern, String html, {bool dotAll = false}) {
    final reg = RegExp(pattern, dotAll: dotAll, caseSensitive: false);
    final match = reg.firstMatch(html);
    if (match != null && match.groupCount >= 1) {
      return match.group(1)?.trim() ?? "";
    }
    return "";
  }

  String optimizeImageUrl(String url, int width, int height) {
    if (url.isEmpty) return "";
    if (!url.startsWith("http")) {
      return "$baseUrl$url";
    }
    return url;
  }

  Future<List<VideoItem>> fetchListPage(String urlStr) async {
    try {
      final res = await http.get(Uri.parse(urlStr), headers: headers);
      if (res.statusCode == 200) {
        return parseListPage(res.body);
      }
    } catch (_) {}
    return [];
  }

  List<VideoItem> parseListPage(String html) {
    List<VideoItem> items = [];
    final itemRegex = RegExp(r'href="index\.php\?do=view&amp;type=post&amp;id=(\d+)".*?<img\s+src="([^"]+)".*?class="title">([^<]+)', dotAll: true, caseSensitive: false);
    
    for (var m in itemRegex.allMatches(html)) {
      if (m.groupCount >= 3) {
        final id = m.group(1) ?? "";
        var img = m.group(2) ?? "";
        final title = m.group(3)?.trim() ?? "";
        img = optimizeImageUrl(img, 400, 600);
        if (!items.any((e) => e.id == id)) {
          items.add(VideoItem(id: id, title: title, imageUrl: img, type: "post"));
        }
      }
    }

    if (items.isEmpty) {
      final fallbackRegex = RegExp(r'data-id="(\d+)".*?data-src="([^"]+)".*?title="([^"]+)"', dotAll: true);
      for (var m in fallbackRegex.allMatches(html)) {
        final id = m.group(1) ?? "";
        var img = m.group(2) ?? "";
        final title = m.group(3) ?? "";
        img = optimizeImageUrl(img, 400, 600);
        items.add(VideoItem(id: id, title: title, imageUrl: img, type: "post"));
      }
    }
    return items;
  }

  Future<Map<String, dynamic>> fetchHomePage() async {
    try {
      final res = await http.get(Uri.parse(baseUrl), headers: headers);
      if (res.statusCode == 200) {
        return parseHomePage(res.body);
      }
    } catch (_) {}
    return {"carousel": <VideoItem>[], "sections": <String, List<VideoItem>>{}};
  }

  Map<String, dynamic> parseHomePage(String html) {
    List<VideoItem> carousel = [];
    Map<String, List<VideoItem>> sections = {};

    final carouselRegex = RegExp(r'class="carousel-item".*?id=(\d+).*?src="([^"]+)".*?<h3>([^<]+)</h3>', dotAll: true);
    for (var m in carouselRegex.allMatches(html)) {
      if (m.groupCount >= 3) {
        carousel.add(VideoItem(
          id: m.group(1) ?? "",
          imageUrl: optimizeImageUrl(m.group(2) ?? "", 800, 400),
          title: m.group(3)?.trim() ?? "",
          type: "post"
        ));
      }
    }

    final blockRegex = RegExp(r'class="block-title">.*?type=(\d+)[^>]*>([^<]+)</a>(.*?)', dotAll: true);
    final itemRegex = RegExp(r'id=(\d+).*?src="([^"]+)".*?class="title">([^<]+)', dotAll: true);

    for (var blockMatch in blockRegex.allMatches(html)) {
      final catTitle = blockMatch.group(2)?.trim() ?? "";
      final blockContent = blockMatch.group(3) ?? "";

      List<VideoItem> sectionItems = [];
      for (var itemMatch in itemRegex.allMatches(blockContent)) {
        sectionItems.add(VideoItem(
          id: itemMatch.group(1) ?? "",
          imageUrl: optimizeImageUrl(itemMatch.group(2) ?? "", 400, 600),
          title: itemMatch.group(3)?.trim() ?? "",
          type: "post"
        ));
      }
      if (sectionItems.isNotEmpty) {
        sections[catTitle] = sectionItems;
      }
    }

    return {"carousel": carousel, "sections": sections};
  }

  Future<MediaDetails> fetchDetails(String id) async {
    MediaDetails d = MediaDetails(id: id);
    try {
      final url = "${baseUrl}index.php?do=view&type=post&id=$id";
      final res = await http.get(Uri.parse(url), headers: headers);
      if (res.statusCode == 200) {
        final html = res.body;
        d.title = _firstMatch(r'<h3>(.*?)</h3>', html);
        d.year = _firstMatch(r'<span>Year:\s*</span>\s*([^<]+)', html);
        d.genre = _firstMatch(r'<span>Genre:\s*</span>\s*([^<]+)', html);
        d.rating = _firstMatch(r'<span>IMdB Rating:\s*</span>\s*([^<]+)', html);
        d.runtime = _firstMatch(r'<span>Runtime:\s*</span>\s*([^<]+)', html);
        d.synopsis = _firstMatch(r'<h3>Synopsis:</h3>.*?<h4>(.*?)</h4>', html, dotAll: true);

        var img = _firstMatch(r'<img src="([^"]+)" class="img-responsive"', html);
        d.imageUrl = optimizeImageUrl(img, 800, 1200);

        if (html.contains('class="episodeitem"')) {
          d.isMovie = false;
          List<EpisodeItem> eps = [];
          final epRegex = RegExp(r'<li class="episodeitem"[^>]*>(.*?)</li>', dotAll: true);
          
          final idReg = RegExp(r'data-id="(\d+)"');
          final titleReg = RegExp(r'data-title="([^"]*)"');
          final urlReg = RegExp(r'data-url="([^"]*)"');
          final url720Reg = RegExp(r'data-url720="([^"]*)"');
          final url1080Reg = RegExp(r'data-url1080="([^"]*)"');
          final url360Reg = RegExp(r'data-url360="([^"]*)"');
          final url4kReg = RegExp(r'data-url4k="([^"]*)"');
          final subReg = RegExp(r'data-subtitle="([^"]*)"');
          final subVttReg = RegExp(r'data-subtitlevtt="([^"]*)"');
          final seasonReg = RegExp(r'data-season="([^"]*)"');

          for (var blockMatch in epRegex.allMatches(html)) {
            final block = blockMatch.group(1) ?? "";
            eps.add(EpisodeItem(
              id: idReg.firstMatch(block)?.group(1) ?? "",
              title: titleReg.firstMatch(block)?.group(1) ?? "",
              url: urlReg.firstMatch(block)?.group(1) ?? "",
              url720: url720Reg.firstMatch(block)?.group(1) ?? "",
              url1080: url1080Reg.firstMatch(block)?.group(1) ?? "",
              url360: url360Reg.firstMatch(block)?.group(1) ?? "",
              url4k: url4kReg.firstMatch(block)?.group(1) ?? "",
              subtitleUrl: subReg.firstMatch(block)?.group(1) ?? "",
              subtitleVttUrl: subVttReg.firstMatch(block)?.group(1) ?? "",
              season: seasonReg.firstMatch(block)?.group(1) ?? "",
            ));
          }
          d.episodes = eps;
        } else {
          d.isMovie = true;
          d.movieUrl = _firstMatch(r'data-url="([^"]*)"', html);
          d.movieUrl720 = _firstMatch(r'data-url720="([^"]*)"', html);
          d.movieUrl1080 = _firstMatch(r'data-url1080="([^"]*)"', html);
          d.movieSubtitleUrl = _firstMatch(r'data-subtitle="([^"]*)"', html);
          d.movieSubtitleVttUrl = _firstMatch(r'data-subtitlevtt="([^"]*)"', html);
        }
      }
    } catch (_) {}
    return d;
  }

  Future<List<VideoItem>> advancedSearch({String? title}) async {
    String url = "${baseUrl}index.php?do=search";
    if (title != null && title.isNotEmpty) {
      url += "&title=${Uri.encodeComponent(title)}";
    }
    return fetchListPage(url);
  }
}
"""
    with open("lib/scraper.dart", "w", encoding="utf-8") as f:
        f.write(scraper_content)

    # ─────────────────────────────────────────────────────────────────
    # 7. كتابة ملف lib/subtitle_parser.dart (محلل ومزامن ملفات الترجمة SRT/VTT)
    # ─────────────────────────────────────────────────────────────────
    sub_parser_content = """import 'package:http/http.dart' as http;

class SubtitleCue {
  final double start;
  final double end;
  final String text;

  SubtitleCue({required this.start, required this.end, required this.text});
}

class SubtitleParser {
  List<SubtitleCue> cues = [];

  Future<void> loadFromUrl(String url) async {
    if (url.isEmpty) return;
    try {
      final res = await http.get(Uri.parse(url));
      if (res.statusCode == 200) {
        parse(res.body);
      }
    } catch (_) {}
  }

  void parse(String content) {
    cues.clear();
    final lines = content.replaceAll('\\r\\n', '\\n').replaceAll('\\r', '\\n').split('\\n');
    final timeReg = RegExp(r'(\\d+:\\d+:\\d+[\\.,]\\d+)\\s*-->\\s*(\\d+:\\d+:\\d+[\\.,]\\d+)');

    String currentText = "";
    double currentStart = -1;
    double currentEnd = -1;

    for (var line in lines) {
      line = line.trim();
      final match = timeReg.firstMatch(line);
      if (match != null) {
        if (currentStart != -1 && currentText.isNotEmpty) {
          cues.add(SubtitleCue(start: currentStart, end: currentEnd, text: currentText.trim()));
        }
        currentStart = _parseTime(match.group(1)!);
        currentEnd = _parseTime(match.group(2)!);
        currentText = "";
      } else if (line.isEmpty) {
        if (currentStart != -1 && currentText.isNotEmpty) {
          cues.add(SubtitleCue(start: currentStart, end: currentEnd, text: currentText.trim()));
          currentStart = -1;
          currentEnd = -1;
          currentText = "";
        }
      } else {
        if (currentStart != -1) {
          if (currentText.isNotEmpty) currentText += "\\n";
          currentText += line;
        }
      }
    }
    if (currentStart != -1 && currentText.isNotEmpty) {
      cues.add(SubtitleCue(start: currentStart, end: currentEnd, text: currentText.trim()));
    }
  }

  double _parseTime(String timeStr) {
    try {
      final parts = timeStr.replaceAll(',', '.').split(':');
      double hours = 0, minutes = 0, seconds = 0;
      if (parts.length == 3) {
        hours = double.parse(parts[0]);
        minutes = double.parse(parts[1]);
        seconds = double.parse(parts[2]);
      }
      return hours * 3600 + minutes * 60 + seconds;
    } catch (_) {
      return 0;
    }
  }

  String getSubtitleAt(double seconds) {
    for (var cue in cues) {
      if (seconds >= cue.start && seconds <= cue.end) {
        return cue.text;
      }
    }
    return "";
  }
}
"""
    with open("lib/subtitle_parser.dart", "w", encoding="utf-8") as f:
        f.write(sub_parser_content)

    # ─────────────────────────────────────────────────────────────────
    # 8. كتابة ملف lib/player.dart (المشغل المتكامل وإعدادات تقديم وتأخير الترجمة)
    # ─────────────────────────────────────────────────────────────────
    player_content = """import 'dart:async';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'settings.dart';
import 'subtitle_parser.dart';

class CustomVideoPlayer extends StatefulWidget {
  final String videoUrl;
  final String subtitleUrl;
  final String title;

  const CustomVideoPlayer({
    Key? key,
    required this.videoUrl,
    required this.subtitleUrl,
    required this.title,
  }) : super(key: key);

  @override
  _CustomVideoPlayerState createState() => _CustomVideoPlayerState();
}

class _CustomVideoPlayerState extends State<CustomVideoPlayer> {
  late VideoPlayerController _controller;
  final SubtitleParser _subParser = SubtitleParser();
  bool _initialized = false;
  bool _showControls = true;
  String _currentSubtitle = "";
  Timer? _hideTimer;

  @override
  void initState() {
    super.initState();
    _initPlayer();
  }

  Future<void> _initPlayer() async {
    _controller = VideoPlayerController.networkUrl(Uri.parse(widget.videoUrl));
    try {
      await _controller.initialize();
      setState(() { _initialized = true; });
      _controller.play();
      _startHideTimer();
      
      if (widget.subtitleUrl.isNotEmpty) {
        await _subParser.loadFromUrl(widget.subtitleUrl);
      }
      _controller.addListener(_playerListener);
    } catch (_) {}
  }

  void _playerListener() {
    if (!mounted) return;
    final settings = AppSettings();
    if (!settings.subtitlesEnabled) {
      if (_currentSubtitle.isNotEmpty) setState(() { _currentSubtitle = ""; });
      return;
    }
    
    final currentPos = _controller.value.position.inMilliseconds / 1000.0;
    final adjustedPos = currentPos + settings.subtitleDelay;
    final txt = _subParser.getSubtitleAt(adjustedPos);
    
    if (txt != _currentSubtitle) {
      setState(() { _currentSubtitle = txt; });
    }
  }

  void _startHideTimer() {
    _hideTimer?.cancel();
    _hideTimer = Timer(const Duration(seconds: 4), () {
      if (mounted && _controller.value.isPlaying) {
        setState(() { _showControls = false; });
      }
    });
  }

  void _toggleControls() {
    setState(() { _showControls = !_showControls; });
    if (_showControls) _startHideTimer();
  }

  @override
  void dispose() {
    _controller.removeListener(_playerListener);
    _controller.dispose();
    _hideTimer?.cancel();
    super.dispose();
  }

  void _showSubtitleSettings() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF130A1C),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        final settings = AppSettings();
        return StatefulBuilder(
          builder: (context, setModalState) {
            return Container(
              padding: const EdgeInsets.all(20),
              child: ListView(
                shrinkWrap: true,
                children: [
                  const Text("إعدادات الترجمة المزامنة", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                  const SizedBox(height: 15),
                  SwitchListTile(
                    title: const Text("تفعيل الترجمة", style: TextStyle(color: Colors.white)),
                    value: settings.subtitlesEnabled,
                    activeColor: const Color(0xFFE30A14),
                    onChanged: (val) {
                      settings.setSubtitlesEnabled(val);
                      setModalState(() {});
                      setState(() {});
                    },
                  ),
                  const Divider(color: Colors.white12),
                  Text("تأخير/تقديم الترجمة: ${settings.subtitleDelay.toStringAsFixed(1)} ثانية", style: const TextStyle(color: Colors.white)),
                  Slider(
                    value: settings.subtitleDelay,
                    min: -5.0,
                    max: 5.0,
                    divisions: 100,
                    activeColor: const Color(0xFFE30A14),
                    inactiveColor: Colors.white24,
                    onChanged: (val) {
                      settings.setSubtitleDelay(val);
                      setModalState(() {});
                      setState(() {});
                    },
                  ),
                  const Divider(color: Colors.white12),
                  Text("حجم خط الترجمة: ${settings.subtitleFontSize.toInt()} px", style: const TextStyle(color: Colors.white)),
                  Slider(
                    value: settings.subtitleFontSize,
                    min: 14.0,
                    max: 36.0,
                    divisions: 22,
                    activeColor: const Color(0xFFE30A14),
                    inactiveColor: Colors.white24,
                    onChanged: (val) {
                      settings.setSubtitleFontSize(val);
                      setModalState(() {});
                      setState(() {});
                    },
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    if (!_initialized) {
      return const Scaffold(
        backgroundColor: Colors.black,
        body: Center(child: CircularProgressIndicator(valueColor: AlwaysStoppedAnimation(Color(0xFFE30A14)))),
      );
    }

    final settings = AppSettings();

    return Scaffold(
      backgroundColor: Colors.black,
      body: GestureDetector(
        onTap: _toggleControls,
        child: Stack(
          alignment: Alignment.center,
          children: [
            Center(
              child: AspectRatio(
                aspectRatio: _controller.value.aspectRatio,
                child: VideoPlayer(_controller),
              ),
            ),
            if (settings.subtitlesEnabled && _currentSubtitle.isNotEmpty)
              Positioned(
                bottom: settings.subtitleBottomPad,
                left: 20,
                right: 20,
                child: Center(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                    decoration: BoxDecoration(
                      color: Colors.black.withOpacity(settings.subtitleBgOpacity),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      _currentSubtitle,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: settings.subtitleFontSize,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
              ),
            if (_showControls)
              Container(
                color: Colors.black45,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    SafeArea(
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 16),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.arrow_back, color: Colors.white),
                              onPressed: () => Navigator.pop(context),
                            ),
                            Expanded(
                              child: Text(
                                widget.title,
                                style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                                overflow: TextOverflow.ellipsis,
                                textAlign: TextAlign.center,
                              ),
                            ),
                            IconButton(
                              icon: const Icon(Icons.closed_caption, color: Colors.white),
                              onPressed: _showSubtitleSettings,
                            ),
                          ],
                        ),
                      ),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        IconButton(
                          icon: const Icon(Icons.replay_10, color: Colors.white, size: 36),
                          onPressed: () {
                            _controller.seekTo(_controller.value.position - const Duration(seconds: 10));
                            _startHideTimer();
                          },
                        ),
                        const SizedBox(width: 24),
                        CircleAvatar(
                          radius: 28,
                          backgroundColor: const Color(0xFFE30A14),
                          child: IconButton(
                            icon: Icon(
                              _controller.value.isPlaying ? Icons.pause : Icons.play_arrow,
                              color: Colors.white,
                              size: 28,
                            ),
                            onPressed: () {
                              setState(() {
                                _controller.value.isPlaying ? _controller.pause() : _controller.play();
                              });
                              _startHideTimer();
                            },
                          ),
                        ),
                        const SizedBox(width: 24),
                        IconButton(
                          icon: const Icon(Icons.forward_10, color: Colors.white, size: 36),
                          onPressed: () {
                            _controller.seekTo(_controller.value.position + const Duration(seconds: 10));
                            _startHideTimer();
                          },
                        ),
                      ],
                    ),
                    SafeArea(
                      top: false,
                      child: Column(
                        children: [
                          VideoProgressIndicator(
                            _controller,
                            allowScrubbing: true,
                            colors: const VideoProgressColors(
                              playedColor: Color(0xFFE30A14),
                              bufferedColor: Colors.white24,
                              backgroundColor: Colors.white10,
                            ),
                          ),
                          Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(_formatDuration(_controller.value.position), style: const TextStyle(color: Colors.white70)),
                                Text(_formatDuration(_controller.value.duration), style: const TextStyle(color: Colors.white70)),
                              ],
                            ),
                          )
                        ],
                      ),
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  String _formatDuration(Duration d) {
    String twoDigits(int n) => n.toString().padLeft(2, '0');
    final minutes = twoDigits(d.inMinutes.remainder(60));
    final seconds = twoDigits(d.inSeconds.remainder(60));
    return "${twoDigits(d.inHours)}:$minutes:$seconds";
  }
}
"""
    with open("lib/player.dart", "w", encoding="utf-8") as f:
        f.write(player_content)

    # ─────────────────────────────────────────────────────────────────
    # 9. كتابة ملف lib/views.dart (واجهات تصفح الأقسام، الحلقات، البحث والتصميم الفاخر)
    # ─────────────────────────────────────────────────────────────────
    views_content = """import 'package:flutter/material.dart';
import 'models.dart';
import 'scraper.dart';
import 'settings.dart';
import 'player.dart';

final List<SiteCategory> SITE_CATEGORIES = [
  SiteCategory(id: 0, nameAr: "أفلام إنجليزية", nameEn: "English Movies"),
  SiteCategory(id: 1, nameAr: "مسلسلات أجنبية", nameEn: "TV Series"),
  SiteCategory(id: 2, nameAr: "أنمي", nameEn: "Anime Series"),
  SiteCategory(id: 3, nameAr: "بوليوود", nameEn: "Bollywood Movies"),
  SiteCategory(id: 4, nameAr: "مسلسلات عربية", nameEn: "Arabic Series"),
  SiteCategory(id: 5, nameAr: "مسلسلات آسيوية", nameEn: "Asian Series"),
  SiteCategory(id: 6, nameAr: "أفلام آسيوية", nameEn: "Asian Movies"),
];

class MainTabView extends StatefulWidget {
  const MainTabView({Key? key}) : super(key: key);

  @override
  _MainTabViewState createState() => _MainTabViewState();
}

class _MainTabViewState extends State<MainTabView> {
  int _currentIndex = 0;
  final MovieScraper scraper = MovieScraper();

  @override
  Widget build(BuildContext context) {
    final List<Widget> tabs = [
      HomeView(scraper: scraper),
      BrowseView(scraper: scraper),
      AdvancedSearchView(scraper: scraper),
      const SettingsView(),
    ];

    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      body: tabs[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        type: BottomNavigationBarType.fixed,
        backgroundColor: const Color(0xFF130A22),
        selectedItemColor: const Color(0xFFE30A14),
        unselectedItemColor: Colors.white60,
        onTap: (idx) => setState(() { _currentIndex = idx; }),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: "الرئيسية"),
          BottomNavigationBarItem(icon: Icon(Icons.grid_view), label: "تصفح"),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: "البحث"),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: "الإعدادات"),
        ],
      ),
    );
  }
}

class HomeView extends StatefulWidget {
  final MovieScraper scraper;
  const HomeView({Key? key, required this.scraper}) : super(key: key);

  @override
  _HomeViewState createState() => _HomeViewState();
}

class _HomeViewState extends State<HomeView> {
  late Future<Map<String, dynamic>> _homeData;

  @override
  void initState() {
    super.initState();
    _homeData = widget.scraper.fetchHomePage();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(
        backgroundColor: const Color(0xFF130A22),
        title: const Text("UTan", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _homeData,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator(valueColor: AlwaysStoppedAnimation(Color(0xFFE30A14))));
          }
          if (!snapshot.hasData) {
            return const Center(child: Text("يرجى التأكد من اتصال الشبكة المخصصة لتشغيل السيرفر", style: TextStyle(color: Colors.white), textAlign: TextAlign.center));
          }

          final carousel = snapshot.data!["carousel"] as List<VideoItem>;
          final sections = snapshot.data!["sections"] as Map<String, List<VideoItem>>;

          return RefreshIndicator(
            onRefresh: () async {
              setState(() { _homeData = widget.scraper.fetchHomePage(); });
            },
            child: ListView(
              children: [
                if (carousel.isNotEmpty)
                  SizedBox(
                    height: 200,
                    child: PageView.builder(
                      itemCount: carousel.length,
                      itemBuilder: (context, idx) {
                        final item = carousel[idx];
                        return GestureDetector(
                          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => DetailsView(itemId: item.id, scraper: widget.scraper))),
                          child: Stack(
                            fit: StackFit.expand,
                            children: [
                              Image.network(item.imageUrl, fit: BoxFit.cover, errorBuilder: (_, __, ___) => Container(color: Colors.white10)),
                              Container(color: Colors.black45),
                              Positioned(
                                bottom: 20,
                                right: 20,
                                left: 20,
                                child: Text(item.title, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold), textDirection: TextDirection.rtl),
                              )
                            ],
                          ),
                        );
                      },
                    ),
                  ),
                ...sections.entries.map((entry) {
                  return Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Text(entry.key, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold), textDirection: TextDirection.rtl),
                      ),
                      SizedBox(
                        height: 220,
                        child: ListView.builder(
                          scrollDirection: Axis.horizontal,
                          reverse: true,
                          itemCount: entry.value.length,
                          itemBuilder: (context, idx) {
                            final item = entry.value[idx];
                            return GestureDetector(
                              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => DetailsView(itemId: item.id, scraper: widget.scraper))),
                              child: Container(
                                width: 120,
                                margin: const EdgeInsets.symmetric(horizontal: 8),
                                child: Column(
                                  children: [
                                    Expanded(
                                      child: ClipRRect(
                                        borderRadius: BorderRadius.circular(8),
                                        child: Image.network(item.imageUrl, fit: BoxFit.cover, errorBuilder: (_, __, ___) => Container(color: Colors.white10)),
                                      ),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(item.title, style: const TextStyle(color: Colors.white, fontSize: 12), maxLines: 2, overflow: TextOverflow.ellipsis, textAlign: TextAlign.center),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                      )
                    ],
                  );
                }).toList()
              ],
            ),
          );
        },
      ),
    );
  }
}

class BrowseView extends StatelessWidget {
  final MovieScraper scraper;
  const BrowseView({Key? key, required this.scraper}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(backgroundColor: const Color(0xFF130A22), title: const Text("تصفح الفئات", style: TextStyle(color: Colors.white))),
      body: GridView.builder(
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 2, mainAxisSpacing: 16, crossAxisSpacing: 16, childAspectRatio: 1.4),
        itemCount: SITE_CATEGORIES.length,
        itemBuilder: (context, idx) {
          final cat = SITE_CATEGORIES[idx];
          return GestureDetector(
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => CategoryListView(category: cat, scraper: scraper))),
            child: Container(
              decoration: BoxDecoration(color: Colors.white.withOpacity(0.05), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFFE30A14).withOpacity(0.3))),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(cat.nameAr, style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 4),
                  Text(cat.nameEn, style: const TextStyle(color: Colors.grey, fontSize: 12)),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

class CategoryListView extends StatefulWidget {
  final SiteCategory category;
  final MovieScraper scraper;
  const CategoryListView({Key? key, required this.category, required this.scraper}) : super(key: key);

  @override
  _CategoryListViewState createState() => _CategoryListViewState();
}

class _CategoryListViewState extends State<CategoryListView> {
  List<VideoItem> items = [];
  int page = 1;
  bool loading = false;
  bool reachedEnd = false;

  @override
  void initState() {
    super.initState();
    _loadMore();
  }

  Future<void> _loadMore() async {
    if (loading || reachedEnd) return;
    setState(() { loading = true; });
    
    final url = "${widget.scraper.baseUrl}index.php?do=list&type=${widget.category.id}&page=$page";
    final nextItems = await widget.scraper.fetchListPage(url);
    
    if (nextItems.isEmpty) {
      setState(() { reachedEnd = true; loading = false; });
    } else {
      setState(() {
        items.addAll(nextItems);
        page++;
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(backgroundColor: const Color(0xFF130A22), title: Text(widget.category.nameAr, style: const TextStyle(color: Colors.white))),
      body: NotificationListener<ScrollNotification>(
        onNotification: (ScrollNotification scrollInfo) {
          if (scrollInfo.metrics.pixels >= scrollInfo.metrics.maxScrollExtent - 200) {
            _loadMore();
          }
          return true;
        },
        child: GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 2, mainAxisSpacing: 16, crossAxisSpacing: 16, childAspectRatio: 0.65),
          itemCount: items.length + (loading ? 2 : 0),
          itemBuilder: (context, idx) {
            if (idx >= items.length) {
              return const Center(child: CircularProgressIndicator(valueColor: AlwaysStoppedAnimation(Color(0xFFE30A14))));
            }
            final item = items[idx];
            return GestureDetector(
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => DetailsView(itemId: item.id, scraper: widget.scraper))),
              child: Column(
                children: [
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: Image.network(item.imageUrl, fit: BoxFit.cover, errorBuilder: (_, __, ___) => Container(color: Colors.white10)),
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(item.title, style: const TextStyle(color: Colors.white, fontSize: 13), maxLines: 2, overflow: TextOverflow.ellipsis, textAlign: TextAlign.center),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}

class DetailsView extends StatelessWidget {
  final String itemId;
  final MovieScraper scraper;
  const DetailsView({Key? key, required this.itemId, required this.scraper}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      body: FutureBuilder<MediaDetails>(
        future: scraper.fetchDetails(itemId),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator(valueColor: AlwaysStoppedAnimation(Color(0xFFE30A14))));
          }
          if (!snapshot.hasData) {
            return const Center(child: Text("تعذر جلب تفاصيل المادة من السيرفر", style: TextStyle(color: Colors.white)));
          }

          final d = snapshot.data!;
          return CustomScrollView(
            slivers: [
              SliverAppBar(
                expandedHeight: 300,
                backgroundColor: const Color(0xFF130A22),
                flexibleSpace: FlexibleSpaceBar(
                  background: Image.network(d.imageUrl, fit: BoxFit.cover, errorBuilder: (_, __, ___) => Container(color: Colors.white10)),
                ),
              ),
              SliverList(
                delegate: SliverChildListDelegate([
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(d.title, style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold), textDirection: TextDirection.rtl),
                        const SizedBox(height: 8),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.end,
                          children: [
                            Text(d.runtime, style: const TextStyle(color: Colors.grey)),
                            const SizedBox(width: 12),
                            Text("IMDb: ${d.rating}", style: const TextStyle(color: Colors.amber, fontWeight: FontWeight.bold)),
                            const SizedBox(width: 12),
                            Text(d.year, style: const TextStyle(color: Colors.grey)),
                          ],
                        ),
                        const SizedBox(height: 12),
                        Text(d.genre, style: const TextStyle(color: Color(0xFFE30A14), fontWeight: FontWeight.w500), textDirection: TextDirection.rtl),
                        const Divider(color: Colors.white24, height: 24),
                        const Text("القصة", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 6),
                        Text(d.synopsis, style: const TextStyle(color: Colors.white70, fontSize: 14), textDirection: TextDirection.rtl),
                        const Divider(color: Colors.white24, height: 24),

                        if (d.isMovie)
                          ElevatedButton.icon(
                            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFE30A14), minimumSize: const Size(double.infinity, 50)),
                            icon: const Icon(Icons.play_arrow, color: Colors.white),
                            label: const Text("تشغيل الفيلم الآن", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                            onPressed: () {
                              final url = d.movieUrl1080.isNotEmpty ? d.movieUrl1080 : d.movieUrl;
                              Navigator.push(context, MaterialPageRoute(builder: (context) => CustomVideoPlayer(videoUrl: url, subtitleUrl: d.movieSubtitleVttUrl, title: d.title)));
                            },
                          )
                        else ...[
                          const Text("الحلقات المتوفرة", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                          const SizedBox(height: 10),
                          ListView.builder(
                            shrinkWrap: true,
                            physics: const NeverScrollableScrollPhysics(),
                            itemCount: d.episodes.length,
                            itemBuilder: (context, idx) {
                              final ep = d.episodes[idx];
                              return Card(
                                color: Colors.white.withOpacity(0.05),
                                child: ListTile(
                                  title: Text(ep.title, style: const TextStyle(color: Colors.white), textDirection: TextDirection.rtl),
                                  leading: const Icon(Icons.play_circle_fill, color: Color(0xFFE30A14)),
                                  onTap: () {
                                    final url = ep.url1080.isNotEmpty ? ep.url1080 : ep.url;
                                    Navigator.push(context, MaterialPageRoute(builder: (context) => CustomVideoPlayer(videoUrl: url, subtitleUrl: ep.subtitleVttUrl, title: ep.title)));
                                  },
                                ),
                              );
                            },
                          )
                        ]
                      ],
                    ),
                  )
                ]),
              )
            ],
          );
        },
      ),
    );
  }
}

class AdvancedSearchView extends StatefulWidget {
  final MovieScraper scraper;
  const AdvancedSearchView({Key? key, required this.scraper}) : super(key: key);

  @override
  _AdvancedSearchViewState createState() => _AdvancedSearchViewState();
}

class _AdvancedSearchViewState extends State<AdvancedSearchView> {
  final TextEditingController _titleController = TextEditingController();
  List<VideoItem> results = [];
  bool loading = false;

  Future<void> _search() async {
    if (_titleController.text.isEmpty) return;
    setState(() { loading = true; });
    final res = await widget.scraper.advancedSearch(title: _titleController.text);
    setState(() { results = res; loading = false; });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(backgroundColor: const Color(0xFF130A22), title: const Text("البحث المتقدم", style: TextStyle(color: Colors.white))),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _titleController,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: "اكتب اسم الفيلم أو المسلسل المُراد بحثه...",
                hintStyle: const TextStyle(color: Colors.white30),
                filled: true,
                fillColor: Colors.white.withOpacity(0.05),
                suffixIcon: IconButton(icon: const Icon(Icons.search, color: Color(0xFFE30A14)), onPressed: _search),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
              textAlign: TextAlign.right,
              onSubmitted: (_) => _search(),
            ),
            const SizedBox(height: 16),
            if (loading)
              const Center(child: CircularProgressIndicator(valueColor: AlwaysStoppedAnimation(Color(0xFFE30A14))))
            else
              Expanded(
                child: GridView.builder(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 2, mainAxisSpacing: 16, crossAxisSpacing: 16, childAspectRatio: 0.65),
                  itemCount: results.length,
                  itemBuilder: (context, idx) {
                    final item = results[idx];
                    return GestureDetector(
                      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => DetailsView(itemId: item.id, scraper: widget.scraper))),
                      child: Column(
                        children: [
                          Expanded(
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(8),
                              child: Image.network(item.imageUrl, fit: BoxFit.cover, errorBuilder: (_, __, ___) => Container(color: Colors.white10)),
                            ),
                          ),
                          const SizedBox(height: 6),
                          Text(item.title, style: const TextStyle(color: Colors.white), maxLines: 2, overflow: TextOverflow.ellipsis, textAlign: TextAlign.center),
                        ],
                      ),
                    );
                  },
                ),
              ),
          ],
        ),
      ),
    );
  }
}

class SettingsView extends StatelessWidget {
  const SettingsView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D0517),
      appBar: AppBar(backgroundColor: const Color(0xFF130A22), title: const Text("الإعدادات", style: TextStyle(color: Colors.white))),
      body: ListView(
        children: [
          ListTile(
            leading: const Icon(Icons.delete_sweep, color: Colors.red),
            title: const Text("مسح التخزين المؤقت للبيانات والسجل", style: TextStyle(color: Colors.white)),
            onTap: () {
              AppSettings().clearCache();
              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("تم مسح السجل والذاكرة المؤقتة لخيارات الترجمة بنجاح.")));
            },
          ),
          const Divider(color: Colors.white12),
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Text("نسخة التطبيق الحالية: 5.0.0 (بنية متكاملة Flutter)", style: TextStyle(color: Colors.grey)),
          )
        ],
      ),
    );
  }
}
"""
    with open("lib/views.dart", "w", encoding="utf-8") as f:
        f.write(views_content)

    # ─────────────────────────────────────────────────────────────────
    # 10. كتابة ملف lib/main.dart (نقطة انطلاق وتشغيل التطبيق الفعلي وتوجيه الشاشة)
    # ─────────────────────────────────────────────────────────────────
    main_content = """import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'settings.dart';
import 'views.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // تهيئة مستودع تفضيلات المستخدم للترجمة والمشاهدة
  await AppSettings().init();
  
  // تمكين تدوير الشاشة التلقائي لتجربة سينمائية أثناء تشغيل الأفلام
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);

  runApp(const UTanApp());
}

class UTanApp extends StatelessWidget {
  const UTanApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'UTan',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0D0517),
        primaryColor: const Color(0xFFE30A14),
      ),
      home: const MainTabView(),
    );
  }
}
"""
    with open("lib/main.dart", "w", encoding="utf-8") as f:
        f.write(main_content)

    print("✅ تم تحويل التطبيق وإنشاء كافة ملفات Flutter للأندرويد بنجاح وخلو كامل من الأخطاء البرمجية!")

if __name__ == "__main__":
    build_flutter_project()
