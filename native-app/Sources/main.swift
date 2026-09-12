import AppKit
import WebKit
import UniformTypeIdentifiers
import Darwin

let appName = "FiM++ Studio"
let starter = ""

struct ExampleEntry: Decodable { let file: String; let title: String }

enum Assets {
    static let examples: [ExampleEntry] = {
        guard let data = try? Data(contentsOf: root.appendingPathComponent("Examples/catalog.json")),
              let entries = try? JSONDecoder().decode([ExampleEntry].self, from: data) else { return [] }
        return entries
    }()
    static var root: URL { Bundle.main.resourceURL! }
    static var java: URL {
        #if arch(arm64)
        let architecture = "arm64"
        #else
        let architecture = "x86_64"
        #endif
        return root.appendingPathComponent("runtimes/\(architecture)/bin/java")
    }
    static var compiler: URL { root.appendingPathComponent("Fimpp.jar") }
    static var guide: URL { root.appendingPathComponent("Guide/index.html") }
}

// Launch the JVM in its own process group so Stop also closes program windows.
if CommandLine.arguments.count > 2 && CommandLine.arguments[1] == "--run-java" {
    _ = setsid()
    let args = Array(CommandLine.arguments.dropFirst(2))
    let pointers = args.map { strdup($0) } + [nil]
    pointers.withUnsafeBufferPointer { buffer in
        _ = execv(args[0], UnsafeMutablePointer(mutating: buffer.baseAddress!))
    }
    perror("Unable to start bundled runtime")
    exit(127)
}

if CommandLine.arguments.contains("--self-test") {
    do {
        guard FileManager.default.isExecutableFile(atPath: Assets.java.path),
              FileManager.default.fileExists(atPath: Assets.guide.path) else {
            throw NSError(domain: "FiMStudio", code: 1, userInfo: [NSLocalizedDescriptionKey: "Bundled resources missing"])
        }
        let process = Process(), pipe = Pipe()
        process.executableURL = Assets.java
        process.arguments = ["-Dfile.encoding=UTF-8", "-jar", Assets.compiler.path,
                             Assets.root.appendingPathComponent("Examples/hello.fimpp").path]
        process.standardOutput = pipe; process.standardError = pipe
        try process.run()
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        process.waitUntilExit()
        let result = String(decoding: data, as: UTF8.self)
        guard process.terminationStatus == 0, result.contains("Hello, Equestria") else {
            throw NSError(domain: "FiMStudio", code: 2, userInfo: [NSLocalizedDescriptionKey: result])
        }
        #if arch(arm64)
        print("PASS FiM++ Studio arm64: bundled Java, latest compiler, examples, offline guide")
        #else
        print("PASS FiM++ Studio x86_64: bundled Java, latest compiler, examples, offline guide")
        #endif
        exit(0)
    } catch { fputs("Self-test failed: \(error)\n", stderr); exit(1) }
}

@objc(FiMDocument)
final class FiMDocument: NSDocument {
    var source = starter
    override class var autosavesInPlace: Bool { true }
    override func makeWindowControllers() {
        let controller = EditorWindow(document: self)
        addWindowController(controller)
    }
    override func data(ofType typeName: String) throws -> Data { Data(source.utf8) }
    override func read(from data: Data, ofType typeName: String) throws {
        guard let text = String(data: data, encoding: .utf8) else {
            throw NSError(domain: NSCocoaErrorDomain, code: NSFileReadInapplicableStringEncodingError,
                          userInfo: [NSLocalizedDescriptionKey: "This letter is not UTF-8 text. Convert it to UTF-8 and open it again."])
        }
        source = text.hasPrefix("\u{feff}") ? String(text.dropFirst()) : text
        for controller in windowControllers { (controller as? EditorWindow)?.loadSource() }
    }
    override func canClose(withDelegate delegate: Any, shouldClose shouldCloseSelector: Selector?, contextInfo: UnsafeMutableRawPointer?) {
        super.canClose(withDelegate: delegate, shouldClose: shouldCloseSelector, contextInfo: contextInfo)
    }
}

final class LineRuler: NSView {
    let ruleThickness: CGFloat = 48
    override var isFlipped: Bool { true }
    weak var editor: NSTextView?
    init(editor: NSTextView, scroll: NSScrollView) {
        self.editor = editor
        super.init(frame: .zero)
    }
    required init(coder: NSCoder) { fatalError() }
    override func draw(_ rect: NSRect) {
        guard let text = editor, let layout = text.layoutManager, let container = text.textContainer else { return }
        NSColor.windowBackgroundColor.setFill(); bounds.fill()
        let content = text.string as NSString
        let visible = text.visibleRect
        let attributes: [NSAttributedString.Key: Any] = [.font: NSFont.monospacedDigitSystemFont(ofSize: 11, weight: .regular), .foregroundColor: NSColor.secondaryLabelColor]
        var index = 0, line = 1
        while index < content.length {
            let glyph = layout.glyphIndexForCharacter(at: index)
            let box = layout.lineFragmentRect(forGlyphAt: glyph, effectiveRange: nil)
            let y = box.origin.y + text.textContainerOrigin.y - visible.origin.y
            if y > bounds.height { break }
            if y + box.height >= 0 {
                let number = "\(line)" as NSString
                let size = number.size(withAttributes: attributes)
                number.draw(at: NSPoint(x: ruleThickness-size.width-12, y: y+1), withAttributes: attributes)
            }
            let next = NSMaxRange(content.lineRange(for: NSRange(location: index, length: 0)))
            if next <= index { break }
            index = next; line += 1
        }
        if content.length == 0 {
            ("1" as NSString).draw(at: NSPoint(x: 32, y: text.textContainerOrigin.y), withAttributes: attributes)
        }
        _ = container
    }
}

final class GuideView: NSView, WKNavigationDelegate {
    let web = WKWebView()
    override init(frame: NSRect) {
        super.init(frame: frame)
        web.navigationDelegate = self
        web.translatesAutoresizingMaskIntoConstraints = false
        addSubview(web)
        NSLayoutConstraint.activate([web.leadingAnchor.constraint(equalTo: leadingAnchor), web.trailingAnchor.constraint(equalTo: trailingAnchor), web.topAnchor.constraint(equalTo: topAnchor), web.bottomAnchor.constraint(equalTo: bottomAnchor)])
        web.loadFileURL(Assets.guide, allowingReadAccessTo: Assets.root.appendingPathComponent("Guide"))
    }
    required init?(coder: NSCoder) { fatalError() }
    override func viewDidChangeEffectiveAppearance() {
        super.viewDidChangeEffectiveAppearance()
        updateGuideAppearance()
    }
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) { updateGuideAppearance() }
    private func updateGuideAppearance() {
        let dark = effectiveAppearance.bestMatch(from: [.aqua, .darkAqua]) == .darkAqua
        web.evaluateJavaScript("document.documentElement.dataset.theme = '\(dark ? "dark" : "light")'")
    }
    func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        if let url = navigationAction.request.url, ["https", "http"].contains(url.scheme ?? "") {
            NSWorkspace.shared.open(url); decisionHandler(.cancel)
        } else { decisionHandler(.allow) }
    }
}

final class EditorWindow: NSWindowController, NSTextViewDelegate, NSWindowDelegate {
    weak var letter: FiMDocument?
    let editor = NSTextView()
    let console = NSTextView()
    let editorScroll = NSScrollView()
    let mainSplit = NSSplitView()
    let workSplit = NSSplitView()
    let guideView = GuideView(frame: .zero)
    let positionLabel = NSTextField(labelWithString: "Ln 1, Col 1")
    let runLabel = NSTextField(labelWithString: "Ready")
    let runButton = NSButton(title: "Run", target: nil, action: nil)
    let stopButton = NSButton(title: "Stop", target: nil, action: nil)
    let input = NSTextField()
    let inputButton = NSButton(title: "Send", target: nil, action: nil)
    var process: Process?
    var processInput: Pipe?
    var outputPipe: Pipe?
    var runFolder: URL?
    var captured = Data()
    var runToken = UUID()
    var stopped = false
    var limitReached = false
    var highlighting = false
    var highlightTimer: Timer?
    var ruler: LineRuler?
    var errorLine: Int?
    var outputEnded = false
    var exitStatus: Int32?
    var guideVisible = true
    var scrollObserver: NSObjectProtocol?
    var inheritedLayout: (frame: NSRect, work: CGFloat, editor: CGFloat, guide: Bool, font: CGFloat)?
    var referenceSplit: CGFloat = 0.5

    init(document: FiMDocument) {
        letter = document
        if let previous = NSApp.keyWindow?.windowController as? EditorWindow, let frame = previous.window?.frame {
            inheritedLayout = (frame, previous.guideVisible ? previous.workSplit.frame.width / max(1, previous.mainSplit.bounds.width) : previous.referenceSplit,
                               previous.workSplit.arrangedSubviews[0].frame.height / max(1, previous.workSplit.bounds.height), previous.guideVisible, previous.editor.font?.pointSize ?? 14)
        }
        let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 1220, height: 810), styleMask: [.titled, .closable, .miniaturizable, .resizable], backing: .buffered, defer: false)
        window.title = "Untitled — FiM++ Studio"
        window.minSize = NSSize(width: 850, height: 570)
        window.tabbingMode = .preferred
        window.isReleasedWhenClosed = false
        super.init(window: window)
        window.delegate = self
        buildUI()
        loadSource()
        window.center()
        window.setFrameAutosaveName("FiMStudioEditor")
        shouldCascadeWindows = false
        if let layout = inheritedLayout { window.setFrame(layout.frame, display: false) }
    }
    required init?(coder: NSCoder) { fatalError() }

    func buildUI() {
        guard let root = window?.contentView else { return }
        let toolbar = NSStackView()
        toolbar.orientation = .horizontal; toolbar.spacing = 10
        toolbar.edgeInsets = NSEdgeInsets(top: 10, left: 16, bottom: 10, right: 16)
        let brand = NSTextField(labelWithString: "✦  FiM++ Studio")
        brand.font = .systemFont(ofSize: 14, weight: .semibold)
        toolbar.addArrangedSubview(brand)
        toolbar.addArrangedSubview(NSView())
        for (title, action, hint) in [("A−", #selector(smallerText(_:)), "Decrease editor font size"), ("A+", #selector(biggerText(_:)), "Increase editor font size")] {
            let button = NSButton(title: title, target: self, action: action)
            button.toolTip = hint; button.setAccessibilityLabel(hint)
            toolbar.addArrangedSubview(button)
        }
        let examples = NSPopUpButton()
        examples.addItem(withTitle: "Examples")
        examples.addItems(withTitles: Assets.examples.map { $0.title })
        examples.target = self; examples.action = #selector(selectExample(_:))
        toolbar.addArrangedSubview(examples)
        let reference = NSButton(title: "Reference", target: self, action: #selector(toggleGuide(_:)))
        reference.image = NSImage(systemSymbolName: "book", accessibilityDescription: "Reference guide")
        reference.imagePosition = .imageLeading
        toolbar.addArrangedSubview(reference)
        stopButton.target = self; stopButton.action = #selector(stopProgram(_:)); stopButton.isEnabled = false
        stopButton.image = NSImage(systemSymbolName: "stop.fill", accessibilityDescription: nil)
        stopButton.imagePosition = .imageLeading
        runButton.target = self; runButton.action = #selector(runProgram(_:))
        runButton.image = NSImage(systemSymbolName: "play.fill", accessibilityDescription: nil)
        runButton.imagePosition = .imageLeading
        runButton.bezelStyle = .rounded; runButton.contentTintColor = .systemPurple
        for button in [stopButton, reference] { button.bezelStyle = .rounded }

        mainSplit.isVertical = true; mainSplit.dividerStyle = .thin
        workSplit.isVertical = false; workSplit.dividerStyle = .thin
        setupEditor()
        let outputPanel = NSView()
        let outputTitle = NSTextField(labelWithString: "OUTPUT")
        outputTitle.font = .systemFont(ofSize: 10, weight: .bold); outputTitle.textColor = .secondaryLabelColor
        runLabel.font = .systemFont(ofSize: 11); runLabel.textColor = .secondaryLabelColor
        let clear = NSButton(title: "Clear Output", target: self, action: #selector(clearConsole(_:)))
        let go = NSButton(title: "Go to error", target: self, action: #selector(goToError(_:)))
        let outputBar = NSStackView(views: [outputTitle, NSView(), runLabel, go, clear, runButton, stopButton])
        for button in [go, clear, runButton, stopButton] { button.controlSize = .small; button.font = .systemFont(ofSize: 11) }
        runLabel.setContentCompressionResistancePriority(.defaultLow, for: .horizontal)
        outputBar.spacing = 5; outputBar.edgeInsets = NSEdgeInsets(top: 7, left: 14, bottom: 7, right: 10)
        console.isEditable = false; console.isSelectable = true
        console.font = .monospacedSystemFont(ofSize: 12, weight: .regular)
        console.textColor = .textColor; console.backgroundColor = .textBackgroundColor
        console.textContainerInset = NSSize(width: 12, height: 8)
        console.isRichText = false
        let outputScroll = NSScrollView()
        outputScroll.hasVerticalScroller = true; outputScroll.documentView = console
        console.autoresizingMask = [.width]; console.isVerticallyResizable = true
        input.placeholderString = "Program input — type here and press Return"
        input.target = self; input.action = #selector(sendInput(_:)); input.isEnabled = false
        input.setAccessibilityLabel("Program input")
        inputButton.target = self; inputButton.action = #selector(sendInput(_:)); inputButton.isEnabled = false
        let eof = NSButton(title: "End input", target: self, action: #selector(endInput(_:)))
        let inputBar = NSStackView(views: [input, inputButton, eof])
        inputBar.spacing = 8; inputBar.edgeInsets = NSEdgeInsets(top: 6, left: 12, bottom: 8, right: 10)
        for view in [outputBar, outputScroll, inputBar] { view.translatesAutoresizingMaskIntoConstraints = false; outputPanel.addSubview(view) }
        NSLayoutConstraint.activate([
            outputBar.heightAnchor.constraint(equalToConstant: 34), inputBar.heightAnchor.constraint(equalToConstant: 36),
            outputBar.leadingAnchor.constraint(equalTo: outputPanel.leadingAnchor), outputBar.trailingAnchor.constraint(equalTo: outputPanel.trailingAnchor), outputBar.topAnchor.constraint(equalTo: outputPanel.topAnchor),
            inputBar.leadingAnchor.constraint(equalTo: outputPanel.leadingAnchor), inputBar.trailingAnchor.constraint(equalTo: outputPanel.trailingAnchor), inputBar.bottomAnchor.constraint(equalTo: outputPanel.bottomAnchor),
            outputScroll.leadingAnchor.constraint(equalTo: outputPanel.leadingAnchor), outputScroll.trailingAnchor.constraint(equalTo: outputPanel.trailingAnchor), outputScroll.topAnchor.constraint(equalTo: outputBar.bottomAnchor), outputScroll.bottomAnchor.constraint(equalTo: inputBar.topAnchor)
        ])
        let editorPanel = NSView()
        let editorTitle = NSTextField(labelWithString: "EDITOR")
        editorTitle.font = .systemFont(ofSize: 10, weight: .bold); editorTitle.textColor = .secondaryLabelColor
        let editorBar = NSStackView(views: [editorTitle, NSView()])
        editorBar.spacing = 6; editorBar.edgeInsets = NSEdgeInsets(top: 7, left: 14, bottom: 7, right: 10)
        for (title, action) in [("Undo", #selector(undoEditor(_:))), ("Redo", #selector(redoEditor(_:))), ("Copy", #selector(copyEditor(_:))), ("Paste", #selector(pasteEditor(_:)))] {
            let button = NSButton(title: title, target: self, action: action)
            button.controlSize = .small; button.font = .systemFont(ofSize: 11)
            editorBar.addArrangedSubview(button)
        }
        editorBar.translatesAutoresizingMaskIntoConstraints = false; editorPanel.addSubview(editorBar)
        NSLayoutConstraint.activate([editorBar.topAnchor.constraint(equalTo: editorPanel.topAnchor), editorBar.leadingAnchor.constraint(equalTo: editorPanel.leadingAnchor), editorBar.trailingAnchor.constraint(equalTo: editorPanel.trailingAnchor), editorBar.heightAnchor.constraint(equalToConstant: 34)])
        if let gutter = ruler {
            gutter.translatesAutoresizingMaskIntoConstraints = false
            editorScroll.translatesAutoresizingMaskIntoConstraints = false
            editorPanel.addSubview(gutter); editorPanel.addSubview(editorScroll)
            NSLayoutConstraint.activate([
                gutter.leadingAnchor.constraint(equalTo: editorPanel.leadingAnchor), gutter.topAnchor.constraint(equalTo: editorBar.bottomAnchor), gutter.bottomAnchor.constraint(equalTo: editorPanel.bottomAnchor), gutter.widthAnchor.constraint(equalToConstant: 48),
                editorScroll.leadingAnchor.constraint(equalTo: gutter.trailingAnchor), editorScroll.trailingAnchor.constraint(equalTo: editorPanel.trailingAnchor), editorScroll.topAnchor.constraint(equalTo: editorBar.bottomAnchor), editorScroll.bottomAnchor.constraint(equalTo: editorPanel.bottomAnchor)
            ])
        }
        workSplit.addArrangedSubview(editorPanel); workSplit.addArrangedSubview(outputPanel)
        workSplit.setHoldingPriority(.defaultLow, forSubviewAt: 0)
        mainSplit.addArrangedSubview(workSplit); mainSplit.addArrangedSubview(guideView)
        mainSplit.setHoldingPriority(.defaultLow, forSubviewAt: 0)
        positionLabel.font = .monospacedDigitSystemFont(ofSize: 10, weight: .regular)
        positionLabel.textColor = .secondaryLabelColor
        let dialect = NSTextField(labelWithString: "FiM++ • Original dialect • UTF-8")
        dialect.font = .systemFont(ofSize: 10); dialect.textColor = .secondaryLabelColor
        let status = NSStackView(views: [positionLabel, NSView(), dialect])
        status.edgeInsets = NSEdgeInsets(top: 6, left: 15, bottom: 6, right: 15)
        for view in [toolbar, mainSplit, status] { view.translatesAutoresizingMaskIntoConstraints = false; root.addSubview(view) }
        NSLayoutConstraint.activate([
            toolbar.heightAnchor.constraint(equalToConstant: 48), status.heightAnchor.constraint(equalToConstant: 26),
            toolbar.leadingAnchor.constraint(equalTo: root.leadingAnchor), toolbar.trailingAnchor.constraint(equalTo: root.trailingAnchor), toolbar.topAnchor.constraint(equalTo: root.topAnchor),
            mainSplit.leadingAnchor.constraint(equalTo: root.leadingAnchor), mainSplit.trailingAnchor.constraint(equalTo: root.trailingAnchor), mainSplit.topAnchor.constraint(equalTo: toolbar.bottomAnchor), mainSplit.bottomAnchor.constraint(equalTo: status.topAnchor),
            status.leadingAnchor.constraint(equalTo: root.leadingAnchor), status.trailingAnchor.constraint(equalTo: root.trailingAnchor), status.bottomAnchor.constraint(equalTo: root.bottomAnchor),
            guideView.widthAnchor.constraint(greaterThanOrEqualToConstant: 260), workSplit.widthAnchor.constraint(greaterThanOrEqualToConstant: 400),
            editorScroll.heightAnchor.constraint(greaterThanOrEqualToConstant: 200), outputPanel.heightAnchor.constraint(greaterThanOrEqualToConstant: 130)
        ])
        DispatchQueue.main.async { [weak self] in
            guard let self = self else { return }
            self.window?.contentView?.layoutSubtreeIfNeeded()
            let work = self.inheritedLayout?.work ?? 0.5
            self.referenceSplit = work
            self.mainSplit.setPosition(self.mainSplit.bounds.width * work, ofDividerAt: 0)
            self.workSplit.setPosition(self.workSplit.bounds.height * (self.inheritedLayout?.editor ?? 0.65), ofDividerAt: 0)
            if let layout = self.inheritedLayout {
                self.editor.font = .monospacedSystemFont(ofSize: layout.font, weight: .regular)
                self.guideVisible = layout.guide; self.guideView.isHidden = !layout.guide
                self.mainSplit.adjustSubviews()
            }
            self.window?.makeFirstResponder(self.editor)
        }
    }
    @objc func undoEditor(_ sender: Any?) { window?.makeFirstResponder(editor); editor.undoManager?.undo() }
    @objc func redoEditor(_ sender: Any?) { window?.makeFirstResponder(editor); editor.undoManager?.redo() }
    @objc func copyEditor(_ sender: Any?) { window?.makeFirstResponder(editor); editor.copy(sender) }
    @objc func pasteEditor(_ sender: Any?) { window?.makeFirstResponder(editor); editor.pasteAsPlainText(sender) }

    func setupEditor() {
        editor.isRichText = false; editor.allowsUndo = true; editor.isEditable = true
        editor.font = .monospacedSystemFont(ofSize: CGFloat(min(40, max(10, UserDefaults.standard.integer(forKey: "EditorFontSize") == 0 ? 14 : UserDefaults.standard.integer(forKey: "EditorFontSize")))), weight: .regular)
        editor.textColor = .textColor; editor.backgroundColor = .textBackgroundColor
        editor.textContainerInset = NSSize(width: 12, height: 16)
        editor.isAutomaticQuoteSubstitutionEnabled = false
        editor.isAutomaticDashSubstitutionEnabled = false
        editor.isAutomaticTextReplacementEnabled = false
        editor.isAutomaticSpellingCorrectionEnabled = false
        editor.isContinuousSpellCheckingEnabled = false
        editor.isGrammarCheckingEnabled = false
        editor.isAutomaticLinkDetectionEnabled = false
        editor.usesFindBar = true
        editor.isVerticallyResizable = true; editor.isHorizontallyResizable = true
        editor.autoresizingMask = [.width]
        editor.minSize = NSSize(width: 0, height: 0)
        editor.maxSize = NSSize(width: CGFloat.greatestFiniteMagnitude, height: CGFloat.greatestFiniteMagnitude)
        editor.textContainer?.containerSize = NSSize(width: 100000, height: CGFloat.greatestFiniteMagnitude)
        editor.textContainer?.widthTracksTextView = false
        editor.delegate = self
        editor.setAccessibilityLabel("FiM++ source editor")
        editorScroll.hasVerticalScroller = true; editorScroll.hasHorizontalScroller = true
        editorScroll.documentView = editor
        ruler = LineRuler(editor: editor, scroll: editorScroll)
        editorScroll.hasVerticalRuler = false; editorScroll.rulersVisible = false
        editorScroll.contentView.postsBoundsChangedNotifications = true
        scrollObserver = NotificationCenter.default.addObserver(forName: NSView.boundsDidChangeNotification, object: editorScroll.contentView, queue: .main) { [weak self] _ in self?.ruler?.needsDisplay = true }
    }
    func loadSource() {
        editor.string = letter?.source ?? starter
        editor.undoManager?.removeAllActions()
        highlight(); updatePosition()
    }
    func textDidChange(_ notification: Notification) {
        guard !highlighting else { return }
        letter?.source = editor.string
        letter?.updateChangeCount(editor.undoManager?.isUndoing == true ? .changeUndone : .changeDone)
        highlightTimer?.invalidate()
        highlightTimer = Timer.scheduledTimer(withTimeInterval: 0.15, repeats: false) { [weak self] _ in self?.highlight() }
        updatePosition(); ruler?.needsDisplay = true
    }
    func textViewDidChangeSelection(_ notification: Notification) { updatePosition() }
    func undoManager(for view: NSTextView) -> UndoManager? { letter?.undoManager }
    func updatePosition() {
        let value = editor.string as NSString
        let cursor = min(editor.selectedRange().location, value.length)
        let prefix = value.substring(to: cursor)
        let line = prefix.reduce(1) { $1 == "\n" ? $0 + 1 : $0 }
        let last = prefix.lastIndex(of: "\n")
        let col = last.map { prefix.distance(from: prefix.index(after: $0), to: prefix.endIndex) + 1 } ?? (prefix.count+1)
        positionLabel.stringValue = "Ln \(line), Col \(col)   ·   \(value.length) characters"
    }
    func highlight() {
        guard let storage = editor.textStorage else { return }
        highlighting = true
        let undo = editor.undoManager
        let undoEnabled = undo?.isUndoRegistrationEnabled == true
        if undoEnabled { undo?.disableUndoRegistration() }
        defer { if undoEnabled { undo?.enableUndoRegistration() } }
        let range = NSRange(location: 0, length: storage.length)
        storage.beginEditing()
        storage.addAttribute(.foregroundColor, value: NSColor.textColor, range: range)
        let colors: [NSColor] = [.systemGreen, .secondaryLabelColor, .systemPurple, .systemOrange]
        for token in FiMSyntax.tokens(editor.string) {
            storage.addAttribute(.foregroundColor, value: colors[token.kind], range: token.range)
        }
        storage.endEditing(); highlighting = false; ruler?.needsDisplay = true
    }
    @objc func toggleGuide(_ sender: Any?) {
        if guideVisible { referenceSplit = workSplit.frame.width / max(1, mainSplit.bounds.width) }
        guideVisible.toggle(); guideView.isHidden = !guideVisible
        mainSplit.adjustSubviews()
        if guideVisible { mainSplit.setPosition(mainSplit.bounds.width * referenceSplit, ofDividerAt: 0) }
    }
    @objc func selectExample(_ sender: NSPopUpButton) {
        let index = sender.indexOfSelectedItem
        if index > 0 && index <= Assets.examples.count { AppDelegate.openExample(Assets.examples[index-1].file) }
        sender.selectItem(at: 0)
    }
    @objc func runProgram(_ sender: Any?) {
        guard process == nil else { return }
        do {
            let folder = FileManager.default.temporaryDirectory.appendingPathComponent("FiMStudio-\(UUID().uuidString)", isDirectory: true)
            try FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
            runFolder = folder
            let snapshot = folder.appendingPathComponent(letter?.fileURL?.lastPathComponent ?? "Untitled.fimpp")
            try Data(editor.string.utf8).write(to: snapshot, options: .atomic)
            let task = Process(), output = Pipe(), stdin = Pipe()
            task.executableURL = Bundle.main.executableURL
            task.arguments = ["--run-java", Assets.java.path, "-Dfile.encoding=UTF-8", "-Xdock:name=FiM++ Studio Program", "-jar", Assets.compiler.path, snapshot.path]
            task.currentDirectoryURL = letter?.fileURL?.deletingLastPathComponent() ?? folder
            var env = ProcessInfo.processInfo.environment
            for key in ["JAVA_TOOL_OPTIONS", "_JAVA_OPTIONS", "JDK_JAVA_OPTIONS", "CLASSPATH"] { env.removeValue(forKey: key) }
            env["JAVA_HOME"] = Assets.java.deletingLastPathComponent().deletingLastPathComponent().path
            task.environment = env
            task.standardOutput = output; task.standardError = output; task.standardInput = stdin
            captured = Data(); console.string = ""; stopped = false; limitReached = false; errorLine = nil; outputEnded = false; exitStatus = nil
            runToken = UUID(); let token = runToken
            output.fileHandleForReading.readabilityHandler = { [weak self] handle in
                let data = handle.availableData
                if data.isEmpty {
                    handle.readabilityHandler = nil
                    DispatchQueue.main.async {
                        guard let self = self, self.runToken == token else { return }
                        self.outputEnded = true
                        if let status = self.exitStatus { self.finish(status: status) }
                    }
                    return
                }
                DispatchQueue.main.async { self?.receive(data, token: token, snapshot: snapshot) }
            }
            task.terminationHandler = { [weak self] ended in
                DispatchQueue.main.async {
                    guard let self = self, self.runToken == token else { return }
                    self.exitStatus = ended.terminationStatus
                    if self.outputEnded { self.finish(status: ended.terminationStatus) }
                    else {
                        DispatchQueue.main.asyncAfter(deadline: .now()+2) {
                            guard self.runToken == token, self.process != nil else { return }
                            // A spawned child may retain stdout after its parent exits.
                            _ = kill(-ended.processIdentifier, SIGTERM)
                            self.finish(status: ended.terminationStatus)
                        }
                    }
                }
            }
            process = task; processInput = stdin; outputPipe = output
            try task.run()
            runButton.isEnabled = false; stopButton.isEnabled = true
            input.isEnabled = true; inputButton.isEnabled = true
            runLabel.stringValue = "Running…"; runLabel.textColor = .systemPurple
        } catch {
            finish(status: 1)
            console.string = "Could not run this letter: \(error.localizedDescription)\n"
        }
    }
    func receive(_ data: Data, token: UUID, snapshot: URL) {
        guard runToken == token, !limitReached else { return }
        let remaining = max(0, 1_000_000-captured.count)
        captured.append(data.prefix(remaining))
        var text = String(decoding: captured, as: UTF8.self)
        text = text.replacingOccurrences(of: snapshot.path, with: letter?.displayName ?? "Untitled.fimpp")
        console.string = text
        console.scrollToEndOfDocument(nil)
        if data.count > remaining {
            limitReached = true
            console.string += "\nOutput limit reached (1 MB). Program stopped.\n"
            stopProgram(nil)
        }
    }
    @objc func stopProgram(_ sender: Any?) {
        guard let task = process, task.isRunning else { return }
        stopped = true
        let pid = task.processIdentifier
        if kill(-pid, SIGTERM) != 0 { task.terminate() }
        runLabel.stringValue = "Stopping…"
        DispatchQueue.main.asyncAfter(deadline: .now()+2) { [weak task] in
            if let task = task, task.isRunning { if kill(-pid, SIGKILL) != 0 { kill(pid, SIGKILL) } }
        }
    }
    func finish(status: Int32) {
        outputPipe?.fileHandleForReading.readabilityHandler = nil
        try? processInput?.fileHandleForWriting.close()
        processInput = nil; outputPipe = nil; process = nil
        runButton.isEnabled = true; stopButton.isEnabled = false
        input.isEnabled = false; inputButton.isEnabled = false
        let text = console.string
        let issue = status != 0 || text.contains("] failure:") || text.contains("] error:") || text.contains("error:") || text.contains("Exception")
        runLabel.stringValue = stopped ? "Stopped" : (issue ? "Check output" : "Finished")
        runLabel.textColor = issue && !stopped ? .systemRed : .secondaryLabelColor
        if let regex = try? NSRegularExpression(pattern: #"\[(\d+)\.\d+\]"#), let match = regex.firstMatch(in: text, range: NSRange(location: 0, length: (text as NSString).length)) {
            errorLine = Int((text as NSString).substring(with: match.range(at: 1)))
        }
        if let folder = runFolder { try? FileManager.default.removeItem(at: folder) }
        runFolder = nil
    }
    @objc func sendInput(_ sender: Any?) {
        guard let pipe = processInput, process?.isRunning == true else { return }
        do { try pipe.fileHandleForWriting.write(contentsOf: Data((input.stringValue+"\n").utf8)); input.stringValue = "" }
        catch { endInput(nil) }
    }
    @objc func endInput(_ sender: Any?) {
        try? processInput?.fileHandleForWriting.close(); processInput = nil
        input.isEnabled = false; inputButton.isEnabled = false
    }
    @objc func clearConsole(_ sender: Any?) { guard process == nil else { return }; captured = Data(); console.string = "" }
    @objc func goToError(_ sender: Any?) {
        guard let line = errorLine else { NSSound.beep(); return }
        let text = editor.string as NSString
        var start = 0
        for _ in 1..<max(1, line) {
            if start >= text.length { break }
            start = NSMaxRange(text.lineRange(for: NSRange(location: start, length: 0)))
        }
        let range = text.lineRange(for: NSRange(location: min(start, text.length), length: 0))
        editor.setSelectedRange(range); editor.scrollRangeToVisible(range); window?.makeFirstResponder(editor)
    }
    func resizeEditor(_ delta: CGFloat) {
        let size = min(40, max(10, (editor.font?.pointSize ?? 14) + delta))
        let undo = editor.undoManager, enabled = editor.undoManager?.isUndoRegistrationEnabled == true
        if enabled { undo?.disableUndoRegistration() }
        editor.font = .monospacedSystemFont(ofSize: size, weight: .regular)
        if enabled { undo?.enableUndoRegistration() }
        UserDefaults.standard.set(Int(size), forKey: "EditorFontSize")
        highlight()
    }
    @objc func biggerText(_ sender: Any?) { resizeEditor(1) }
    @objc func smallerText(_ sender: Any?) { resizeEditor(-1) }
    func windowWillClose(_ notification: Notification) {
        stopProgram(nil); highlightTimer?.invalidate()
        if let observer = scrollObserver { NotificationCenter.default.removeObserver(observer) }
        scrollObserver = nil
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate, NSMenuItemValidation {
    private let appearanceKey = "StudioAppearance"
    private let appearanceModes = ["system", "light", "dark"]
    private func applyAppearance() {
        switch UserDefaults.standard.string(forKey: appearanceKey) {
        case "light": NSApp.appearance = NSAppearance(named: .aqua)
        case "dark": NSApp.appearance = NSAppearance(named: .darkAqua)
        default: NSApp.appearance = nil
        }
    }
    @objc func selectAppearance(_ sender: NSMenuItem) {
        guard appearanceModes.indices.contains(sender.tag) else { return }
        UserDefaults.standard.set(appearanceModes[sender.tag], forKey: appearanceKey)
        applyAppearance()
    }
    func validateMenuItem(_ item: NSMenuItem) -> Bool {
        if item.action == #selector(selectAppearance(_:)), appearanceModes.indices.contains(item.tag) {
            item.state = (UserDefaults.standard.string(forKey: appearanceKey) ?? "system") == appearanceModes[item.tag] ? .on : .off
        }
        return true
    }
    var guideWindow: NSWindow?
    static func openExample(_ name: String) {
        do {
            let source = try String(contentsOf: Assets.root.appendingPathComponent("Examples/\(name).fimpp"), encoding: .utf8)
            let doc = FiMDocument(); doc.source = source
            NSDocumentController.shared.addDocument(doc)
            doc.makeWindowControllers(); doc.showWindows(); doc.updateChangeCount(.changeDone)
        } catch { NSApp.presentError(error) }
    }
    func applicationWillFinishLaunching(_ notification: Notification) { applyAppearance(); setupMenus() }
    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.regular)
        NSApp.activate(ignoringOtherApps: true)
        if NSDocumentController.shared.documents.isEmpty { NSDocumentController.shared.newDocument(nil) }
    }
    func applicationShouldOpenUntitledFile(_ sender: NSApplication) -> Bool { true }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { false }
    func applicationWillTerminate(_ notification: Notification) {
        for doc in NSDocumentController.shared.documents {
            for controller in doc.windowControllers { (controller as? EditorWindow)?.stopProgram(nil) }
        }
    }
    @objc func openGuide(_ sender: Any?) {
        if guideWindow == nil {
            let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 900, height: 760), styleMask: [.titled, .closable, .miniaturizable, .resizable], backing: .buffered, defer: false)
            window.title = "FiM++ Coding Reference"; window.contentView = GuideView(frame: window.contentView!.bounds)
            window.isReleasedWhenClosed = false; window.center(); guideWindow = window
        }
        guideWindow?.makeKeyAndOrderFront(nil)
    }
    @objc func about(_ sender: Any?) {
        NSApp.orderFrontStandardAboutPanel(options: [.applicationName: appName, .applicationVersion: Bundle.main.object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String ?? "1.2.0", .credits: NSAttributedString(string: "Created by: RyogaTwo\n\nA native home for letters to Princess Celestia.\nIncludes the original FiM++ dialect, an offline guide,\nand native runtimes for Intel and Apple Silicon.\n\nFiM++ © Karol Stasiak and contributors · GPLv3+\nEclipse Temurin · GPLv2 with Classpath Exception")])
    }
    func setupMenus() {
        let bar = NSMenu(); NSApp.mainMenu = bar
        func menu(_ title: String) -> NSMenu {
            let item = NSMenuItem(); bar.addItem(item)
            let child = NSMenu(title: title); item.submenu = child; return child
        }
        func item(_ menu: NSMenu, _ title: String, _ action: Selector, _ key: String = "", _ flags: NSEvent.ModifierFlags = .command, _ target: AnyObject? = nil) {
            let i = NSMenuItem(title: title, action: action, keyEquivalent: key)
            i.keyEquivalentModifierMask = flags; i.target = target; menu.addItem(i)
        }
        let app = menu(appName)
        item(app, "About FiM++ Studio", #selector(about(_:)), "", .command, self)
        app.addItem(.separator())
        item(app, "Hide FiM++ Studio", #selector(NSApplication.hide(_:)), "h")
        item(app, "Hide Others", #selector(NSApplication.hideOtherApplications(_:)), "h", [.command, .option])
        item(app, "Show All", #selector(NSApplication.unhideAllApplications(_:)))
        app.addItem(.separator()); item(app, "Quit FiM++ Studio", #selector(NSApplication.terminate(_:)), "q")
        let file = menu("File")
        item(file, "New Letter", #selector(NSDocumentController.newDocument(_:)), "n")
        item(file, "Open…", #selector(NSDocumentController.openDocument(_:)), "o")
        file.addItem(.separator())
        item(file, "Save", #selector(NSDocument.save(_:)), "s")
        item(file, "Save As…", #selector(NSDocument.saveAs(_:)), "s", [.command, .shift])
        item(file, "Revert to Saved…", #selector(NSDocument.revertToSaved(_:)))
        file.addItem(.separator()); item(file, "Close", #selector(NSWindow.performClose(_:)), "w")
        let edit = menu("Edit")
        item(edit, "Undo", Selector(("undo:")), "z")
        item(edit, "Redo", Selector(("redo:")), "z", [.command, .shift])
        edit.addItem(.separator())
        item(edit, "Cut", #selector(NSText.cut(_:)), "x")
        item(edit, "Copy", #selector(NSText.copy(_:)), "c")
        item(edit, "Paste", #selector(NSText.paste(_:)), "v")
        item(edit, "Select All", #selector(NSText.selectAll(_:)), "a")
        edit.addItem(.separator())
        let find = NSMenuItem(title: "Find…", action: #selector(NSTextView.performFindPanelAction(_:)), keyEquivalent: "f")
        find.tag = NSTextFinder.Action.showFindInterface.rawValue; edit.addItem(find)
        let program = menu("Program")
        item(program, "Run Letter", #selector(EditorWindow.runProgram(_:)), "r")
        item(program, "Stop", #selector(EditorWindow.stopProgram(_:)), ".")
        item(program, "Go to Error", #selector(EditorWindow.goToError(_:)))
        let view = menu("View")
        item(view, "Toggle Reference", #selector(EditorWindow.toggleGuide(_:)), "r", [.command, .shift])
        item(view, "Larger Text", #selector(EditorWindow.biggerText(_:)), "+")
        item(view, "Smaller Text", #selector(EditorWindow.smallerText(_:)), "-")
        view.addItem(.separator())
        let appearanceItem = NSMenuItem(title: "Appearance", action: nil, keyEquivalent: "")
        let appearanceMenu = NSMenu(title: "Appearance")
        for (index, title) in ["Follow System", "Light", "Dark"].enumerated() {
            let choice = NSMenuItem(title: title, action: #selector(selectAppearance(_:)), keyEquivalent: "")
            choice.tag = index; choice.target = self; appearanceMenu.addItem(choice)
        }
        appearanceItem.submenu = appearanceMenu; view.addItem(appearanceItem)
        let windows = menu("Window"); NSApp.windowsMenu = windows
        item(windows, "Minimize", #selector(NSWindow.performMiniaturize(_:)), "m")
        item(windows, "Zoom", #selector(NSWindow.performZoom(_:)))
        let help = menu("Help"); NSApp.helpMenu = help
        item(help, "FiM++ Coding Reference", #selector(openGuide(_:)), "?", .command, self)
    }
}

let application = NSApplication.shared
let delegate = AppDelegate()
application.delegate = delegate
application.run()
