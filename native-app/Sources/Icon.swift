import AppKit
let output = CommandLine.arguments[1]
try FileManager.default.createDirectory(atPath: output, withIntermediateDirectories: true)
for size in [16,32,64,128,256,512,1024] {
    let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    let context = NSGraphicsContext.current!.cgContext
    context.scaleBy(x: CGFloat(size)/1024, y: CGFloat(size)/1024)
    let rect=NSRect(x:44,y:44,width:936,height:936)
    let bg=NSBezierPath(roundedRect:rect,xRadius:208,yRadius:208)
    NSGradient(starting:NSColor(calibratedRed:0.30,green:0.19,blue:0.46,alpha:1),ending:NSColor(calibratedRed:0.13,green:0.09,blue:0.23,alpha:1))!.draw(in:bg,angle:90)
    NSColor(calibratedRed:0.63,green:0.48,blue:0.79,alpha:1).setFill()
    NSBezierPath(roundedRect:NSRect(x:238,y:213,width:538,height:614),xRadius:48,yRadius:48).fill()
    NSColor(calibratedRed:0.99,green:0.97,blue:0.91,alpha:1).setFill()
    NSBezierPath(roundedRect:NSRect(x:203,y:246,width:538,height:614),xRadius:48,yRadius:48).fill()
    NSColor(calibratedRed:0.86,green:0.80,blue:0.68,alpha:1).setStroke()
    for y in [704,646,588] {
        let line=NSBezierPath();line.move(to:NSPoint(x:285,y:y));line.line(to:NSPoint(x:y==588 ? 516 : 651,y:y));line.lineWidth=17;line.lineCapStyle = .round;line.stroke()
    }
    let symbol="›_" as NSString
    symbol.draw(at:NSPoint(x:276,y:352),withAttributes:[.font:NSFont.monospacedSystemFont(ofSize:151,weight:.semibold),.foregroundColor:NSColor(calibratedRed:0.43,green:0.26,blue:0.60,alpha:1)])
    NSColor(calibratedRed:0.95,green:0.76,blue:0.38,alpha:1).setFill()
    let star=NSBezierPath();let center=NSPoint(x:759,y:278)
    for i in 0..<8 {
        let angle=Double(i)*Double.pi/4;let radius:Double=i%2==0 ? 125:43
        let point=NSPoint(x:center.x+cos(angle)*radius,y:center.y+sin(angle)*radius)
        if i==0{star.move(to:point)}else{star.line(to:point)}
    }
    star.close();star.fill()
    NSGraphicsContext.restoreGraphicsState()
    let data=bitmap.representation(using:.png,properties:[:])!
    let filename=size==1024 ? "icon_512x512@2x.png" : "icon_\(size)x\(size).png"
    if size != 64 { try data.write(to:URL(fileURLWithPath:output).appendingPathComponent(filename)) }
    if [32,64,256,512].contains(size) {
        try data.write(to:URL(fileURLWithPath:output).appendingPathComponent("icon_\(size/2)x\(size/2)@2x.png"))
    }
}
