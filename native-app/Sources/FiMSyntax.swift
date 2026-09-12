import Foundation

// Keep this pattern aligned with windows-app/app/syntax.js; parity is regression tested.
enum FiMSyntax {
    struct Token { let range: NSRange; let kind: Int }
    static let regex = try! NSRegularExpression(pattern: #"("[^"]*(?:"|$))|(\([^)]*(?:\)|$)|(?<![A-Za-z\x27-])(?:(?:p\.)+s\.|p(?:\.?s)+\.|p+s+:?(?=\s|$))[^\r\n]*|\bby\s+the\s+way\b[^.!?]*(?:[.!?]|$)|,\s*because\b[^.!?]*(?:[.!?]|$))|(\b(?:dear\s+princess\s+celestia|today\s+i\s+learned|your\s+faithful\s+student|did\s+you\s+know|i\s+learned|that's\s+about|that's\s+what\s+i\s+did|i\s+did\s+this\s+while|i\s+did\s+this\s+instead|i\s+did\s+this|in\s+the\s+end|it\s+didn't\s+work|but\s+i\s+knew\s+why|when|i\s+quickly\s+said|i\s+quickly\s+wrote|i\s+quickly\s+sang|i\s+said|i\s+wrote|i\s+sang|i\s+enchanted|i\s+asked|i\s+told|i\s+woke\s+up|i\s+found\s+a\s+book|i\s+read\s+about|i\s+scribbled|i\s+noted|i\s+gave|i\s+sold|i\s+took|i\s+got|i\s+stole|i\s+also\s+did|i\s+also\s+made|i\s+also\s+caused|i\s+did|i\s+made|i\s+caused|yes|and|either|or|not|is|are|likes|like|got|more|less|fewer|with|of\s+each|everything|everypony|anything|anypony)\b)|(\b(?:[0-9]+(?:st|nd|rd|th)?|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth)\b)"#, options: [.caseInsensitive])
    static func tokens(_ text: String) -> [Token] {
        regex.matches(in: text, range: NSRange(location: 0, length: (text as NSString).length)).map { match in
            let kind = (1...4).first { match.range(at: $0).location != NSNotFound }! - 1
            return Token(range: match.range, kind: kind)
        }
    }
}
