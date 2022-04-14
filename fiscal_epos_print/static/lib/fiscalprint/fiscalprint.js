//
// ePOS-Print and Fiscal Print API
//
// Version 1.1.1
//
// Copyright (C) SEIKO EPSON CORPORATION 2018. All rights reserved.
//

// 06/12/2012	1.0.0
// First release.

// 01/09/2014	1.0.1
// 1. Added send timeout parameter (argument).
// 2. Added onreceive res_add argument so that complete response can also be returned.
// 3. onerror response generates FP_NO_ANSWER_NETWORK fixed text instead of xhr response.
// 4. encodeBase64Binary object added for future use.


// 23/03/2018	1.1.0
// 1. Added empty node exception handling.
// 2. Added "statusText" string field in result variable as "status" field is Integer which doesn't manage text
//    present in certain replies.
// 3. Added callMode argument in send method so that either asynchronous or synchronous mode can be selected.
//    Use "async" for asynchronous otherwise defaults to synchronous.
//    If null, defaults to async.
//    Timeout only valid for async mode.

// 14/06/2018	1.1.1
// 1. Added responseText and responseXML fields to onerror result object.


// 06/07/2018	1.1.2
// 1. Added radix to parseInt for best practice.

(function (window)
{

    //
    // Function: ePOSBuilder constructor
    // Description: initialize an ePOS-Print XML Builder object
    // Parameters:  none
    // Return:      none
    //
    function ePOSBuilder() {
        // properties
        this.message = '';
        // constants
        this.FONT_A = 'font_a';
        this.FONT_B = 'font_b';
        this.FONT_C = 'font_c';
        this.FONT_SPECIAL_A = 'special_a';
        this.FONT_SPECIAL_B = 'special_b';
        this.ALIGN_LEFT = 'left';
        this.ALIGN_CENTER = 'center';
        this.ALIGN_RIGHT = 'right';
        this.COLOR_NONE = 'none';
        this.COLOR_1 = 'color_1';
        this.COLOR_2 = 'color_2';
        this.COLOR_3 = 'color_3';
        this.COLOR_4 = 'color_4';
        this.BARCODE_UPC_A = 'upc_a';
        this.BARCODE_UPC_E = 'upc_e';
        this.BARCODE_EAN13 = 'ean13';
        this.BARCODE_JAN13 = 'jan13';
        this.BARCODE_EAN8 = 'ean8';
        this.BARCODE_JAN8 = 'jan8';
        this.BARCODE_CODE39 = 'code39';
        this.BARCODE_ITF = 'itf';
        this.BARCODE_CODABAR = 'codabar';
        this.BARCODE_CODE93 = 'code93';
        this.BARCODE_CODE128 = 'code128';
        this.BARCODE_GS1_128 = 'gs1_128';
        this.BARCODE_GS1_DATABAR_OMNIDIRECTIONAL = 'gs1_databar_omnidirectional';
        this.BARCODE_GS1_DATABAR_TRUNCATED = 'gs1_databar_truncated';
        this.BARCODE_GS1_DATABAR_LIMITED = 'gs1_databar_limited';
        this.BARCODE_GS1_DATABAR_EXPANDED = 'gs1_databar_expanded';
        this.HRI_NONE = 'none';
        this.HRI_ABOVE = 'above';
        this.HRI_BELOW = 'below';
        this.HRI_BOTH = 'both';
        this.SYMBOL_PDF417_STANDARD = 'pdf417_standard';
        this.SYMBOL_PDF417_TRUNCATED = 'pdf417_truncated';
        this.SYMBOL_QRCODE_MODEL_1 = 'qrcode_model_1';
        this.SYMBOL_QRCODE_MODEL_2 = 'qrcode_model_2';
        this.SYMBOL_MAXICODE_MODE_2 = 'maxicode_mode_2';
        this.SYMBOL_MAXICODE_MODE_3 = 'maxicode_mode_3';
        this.SYMBOL_MAXICODE_MODE_4 = 'maxicode_mode_4';
        this.SYMBOL_MAXICODE_MODE_5 = 'maxicode_mode_5';
        this.SYMBOL_MAXICODE_MODE_6 = 'maxicode_mode_6';
        this.SYMBOL_GS1_DATABAR_STACKED = 'gs1_databar_stacked';
        this.SYMBOL_GS1_DATABAR_STACKED_OMNIDIRECTIONAL = 'gs1_databar_stacked_omnidirectional';
        this.SYMBOL_GS1_DATABAR_EXPANDED_STACKED = 'gs1_databar_expanded_stacked';
        this.LEVEL_0 = 'level_0';
        this.LEVEL_1 = 'level_1';
        this.LEVEL_2 = 'level_2';
        this.LEVEL_3 = 'level_3';
        this.LEVEL_4 = 'level_4';
        this.LEVEL_5 = 'level_5';
        this.LEVEL_6 = 'level_6';
        this.LEVEL_7 = 'level_7';
        this.LEVEL_8 = 'level_8';
        this.LEVEL_L = 'level_l';
        this.LEVEL_M = 'level_m';
        this.LEVEL_Q = 'level_q';
        this.LEVEL_H = 'level_h';
        this.LEVEL_DEFAULT = 'default';
        this.LINE_THIN = 'thin';
        this.LINE_MEDIUM = 'medium';
        this.LINE_THICK = 'thick';
        this.LINE_THIN_DOUBLE = 'thin_double';
        this.LINE_MEDIUM_DOUBLE = 'medium_double';
        this.LINE_THICK_DOUBLE = 'thick_double';
        this.DIRECTION_LEFT_TO_RIGHT = 'left_to_right';
        this.DIRECTION_BOTTOM_TO_TOP = 'bottom_to_top';
        this.DIRECTION_RIGHT_TO_LEFT = 'right_to_left';
        this.DIRECTION_TOP_TO_BOTTOM = 'top_to_bottom';
        this.CUT_NO_FEED = 'no_feed';
        this.CUT_FEED = 'feed';
        this.CUT_RESERVE = 'reserve';
        this.DRAWER_1 = 'drawer_1';
        this.DRAWER_2 = 'drawer_2';
        this.PULSE_100 = 'pulse_100';
        this.PULSE_200 = 'pulse_200';
        this.PULSE_300 = 'pulse_300';
        this.PULSE_400 = 'pulse_400';
        this.PULSE_500 = 'pulse_500';
        this.PATTERN_NONE = 'none';
        this.PATTERN_A = 'pattern_a';
        this.PATTERN_B = 'pattern_b';
        this.PATTERN_C = 'pattern_c';
        this.PATTERN_D = 'pattern_d';
        this.PATTERN_E = 'pattern_e';
        this.PATTERN_ERROR = 'error';
        this.PATTERN_PAPER_END = 'paper_end';
    }

    //
    // Function: addFeedUnit method
    // Description: append the XML element to print and feed paper
    // Parameters:
    //      unit    unsignedbyte    paper feed amount (units)
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addFeedUnit = function (unit) {
        // create empty string
        var s = '';
        // check parameter
        s += getUByteAttr('unit', unit);
        // append element
        this.message += '<feed' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addFeedLine method
    // Description: append the XML element to print and feed n lines
    // Parameters:
    //      line    unsignedbyte    paper feed amount (lines)
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addFeedLine = function (line) {
        // create empty string
        var s = '';
        // check parameter
        s += getUByteAttr('line', line);
        // append element
        this.message += '<feed' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addText method
    // Description: append the XML element to print characters
    // Parameters:
    //      data    string      characters
    // Return:      object      ePOSBuilder object
    //
    ePOSBuilder.prototype.addText = function (data) {
        // append element
        this.message += '<text>' + encodeXmlEntity(data) + '</text>';
        // return builder object
        return this;
    }

    //
    // Function: addTextLang method
    // Description: append the XML element to select language
    // Parameters:
    //      lang    string      language code and country code (en, en-US, ja, ja-JP, etc.)
    // Return:      object      ePOSBuilder object
    //
    ePOSBuilder.prototype.addTextLang = function (lang) {
        // append element
        this.message += '<text lang="' + lang + '"/>';
        // return builder object
        return this;
    }

    //
    // Function: addTextAlign method
    // Description: append the XML element to set alignment
    // Parameters:
    //      align   string      alignment (ALIGN_* constants)
    // Return:      object      ePOSBuilder object
    // Throws:      object      invalid parameter
    //
    ePOSBuilder.prototype.addTextAlign = function (align) {
        // create empty string
        var s = '';
        // check parameter
        s += getEnumAttr('align', align, regexAlign);
        // append element
        this.message += '<text' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addTextRotate method
    // Description: append the XML element to turn upside-down print mode on/off
    // Parameters:
    //      rotate      boolean     when true, upside-down print mode is turned on
    // Return:          object      ePOSBuilder object
    // Throws:          object      invalid parameter
    //
    ePOSBuilder.prototype.addTextRotate = function (rotate) {
        // create empty string
        var s = '';
        // check parameter
        s += getBoolAttr('rotate', rotate);
        // append element
        this.message += '<text' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addTextLineSpace method
    // Description: append the XML element to set line spacing
    // Parameters:
    //      linespc     unsignedByte    the amount of line spacing
    // Return:          object          ePOSBuilder object
    // Throws:          object          invalid parameter
    //
    ePOSBuilder.prototype.addTextLineSpace = function (linespc) {
        // create empty string
        var s = '';
        // check parameter
        s += getUByteAttr('linespc', linespc);
        // append element
        this.message += '<text' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addTextFont method
    // Description: append the XML element to select character font
    // Parameters:
    //      font    string      font (FONT_* constants)
    // Return:      object      ePOSBuilder object
    // Throws:      object      invalid parameter
    //
    ePOSBuilder.prototype.addTextFont = function (font) {
        // create empty string
        var s = '';
        // check parameter
        s += getEnumAttr('font', font, regexFont);
        // append element
        this.message += '<text' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addTextSmooth method
    // Description: append the XML element to turn smoothing mode on/off
    // Parameters:
    //      smooth      boolean         when true, smoothing mode is turned on
    // Return:          object          ePOSBuilder object
    // Throws:          object          invalid parameter
    //
    ePOSBuilder.prototype.addTextSmooth = function (smooth) {
        // create empty string
        var s = '';
        // check parameter
        s += getBoolAttr('smooth', smooth);
        // append element
        this.message += '<text' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addTextDouble method
    // Description: append the XML element to turn double-wide/double-high mode on/off
    // Parameters:
    //      dw       boolean    when true, double-wide mode is turned on [option]
    //      dh       boolean    when true, double-high mode is turned on [option]
    // Return:          object          ePOSBuilder object
    // Throws:          object          invalid parameter
    //
    ePOSBuilder.prototype.addTextDouble = function (dw, dh) {
        // create empty string
        var s = '';
        // check parameter (option)
        if (dw !== undefined) {
            s += getBoolAttr('dw', dw);
        }
        // check parameter (option)
        if (dh !== undefined) {
            s += getBoolAttr('dh', dh);
        }
        // append element
        this.message += '<text' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addTextSize method
    // Description: append the XML element to select character size
    // Parameters:
    //      width       unsignedByte    character width (1 to 8) [option]
    //      height      unsignedByte    character height (1 to 8) [option]
    // Return:          object          ePOSBuilder object
    // Throws:          object          invalid parameter
    //
    ePOSBuilder.prototype.addTextSize = function (width, height) {
        // create empty string
        var s = '';
        // check parameter (option)
        if (width !== undefined) {
            s += getIntAttr('width', width, 1, 8);
        }
        // check parameter (option)
        if (height !== undefined) {
            s += getIntAttr('height', height, 1, 8);
        }
        // append element
        this.message += '<text' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addTextStyle method
    // Description: append the XML element to select character style
    // Parameters:
    //      reverse     boolean     when true, black/white reverse print mode is turned on [option]
    //      ul          boolean     when true, underline mode is turned on [option]
    //      em          boolean     when true, emphasized mode is turned on [option]
    //      color       string      color (COLOR_* constants) [option]
    // Return:          object      ePOSBuilder object
    // Throws:          object      invalid parameter
    //
    ePOSBuilder.prototype.addTextStyle = function (reverse, ul, em, color) {
        // create empty string
        var s = '';
        // check parameter (option)
        if (reverse !== undefined) {
            s += getBoolAttr('reverse', reverse);
        }
        // check parameter (option)
        if (ul !== undefined) {
            s += getBoolAttr('ul', ul);
        }
        // check parameter (option)
        if (em !== undefined) {
            s += getBoolAttr('em', em);
        }
        // check parameter (option)
        if (color !== undefined) {
            s += getEnumAttr('color', color, regexColor);
        }
        // append element
        this.message += '<text' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addTextPosition method
    // Description: append the XML element to set absolute print position
    // Parameters:
    //      x       unsignedShort   X start position
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addTextPosition = function (x) {
        // create empty string
        var s = '';
        // check parameter
        s += getUShortAttr('x', x);
        // append element
        this.message += '<text' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addImage method
    // Description: append the XML element to print the graphics data (raster format)
    // Parameters:
    //      context     object          the 2-D context of HTML 5 Canvas
    //      x           unsignedShort   X start position
    //      y           unsignedShort   Y start position
    //      width       unsignedShort   horizontal size
    //      height      unsignedShort   vertical size
    //      color       string          color (COLOR_* constants) [option]
    // Return:          object          ePOSBuilder object
    // Throws:          object          invalid parameter
    //
    ePOSBuilder.prototype.addImage = function (context, x, y, width, height, color) {
        // create empty string
        var s = '';
        // check parameter
        getUShortAttr('x', x);
        // check parameter
        getUShortAttr('y', y);
        // check parameter
        s += getUShortAttr('width', width);
        // check parameter
        s += getUShortAttr('height', height);
        // check parameter (option)
        if (color !== undefined) {
            s += getEnumAttr('color', color, regexColor);
        }
        // create image data
        var image = encodeRasterImage(context.getImageData(x, y, width, height).data, width, height);
        // append element
        this.message += '<image' + s + '>' + encodeBase64Binary(image) + '</image>';
        // return builder object
        return this;
    }

    //
    // Function: addLogo method
    // Description: append the XML element to print specified NV graphics data
    // Parameters:
    //      key1    unsignedShort   key code 1
    //      key2    unsignedShort   key code 2
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addLogo = function (key1, key2) {
        // create empty string
        var s = '';
        // check parameter
        s += getUByteAttr('key1', key1);
        // check parameter
        s += getUByteAttr('key2', key2);
        // append element
        this.message += '<logo' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addBarcode method
    // Description: append the XML element to print bar code
    // Parameters:
    //      data        object          bar code data (characters, escape sequences '\xnn', '\\')
    //      type        string          bar code type (BARCODE_* constants)
    //      hri         string          print position of HRI characters (HRI_* constants) [option]
    //      font        string          font for HRI characters (FONT_* constants) [option]
    //      width       unsignedByte    bar code module width [option]
    //      height      unsignedByte    bar code module height [option]
    // Return:          object          ePOSBuilder object
    // Throws:          object          invalid parameter
    //
    ePOSBuilder.prototype.addBarcode = function (data, type, hri, font, width, height) {
        // create empty string
        var s = '';
        // check parameter
        s += getEnumAttr('type', type, regexBarcode);
        // check parameter (option)
        if (hri !== undefined) {
            s += getEnumAttr('hri', hri, regexHri);
        }
        // check parameter (option)
        if (font !== undefined) {
            s += getEnumAttr('font', font, regexFont);
        }
        // check parameter (option)
        if (width !== undefined) {
            s += getUByteAttr('width', width);
        }
        // check parameter (option)
        if (height !== undefined) {
            s += getUByteAttr('height', height);
        }
        // append element
        this.message += '<barcode' + s + '>' + escapeText(encodeXmlEntity(data)) + '</barcode>';
        // return builder object
        return this;
    }

    //
    // Function: addSymbol method
    // Description: append the XML element to print two dimension code
    // Parameters:
    //      data        object          symbol data (characters, escape sequences '\xnn', '\\')
    //      type        string          symbol type (SYMBOL_* constants)
    //      level       string          error correction level (LEVEL_* constants) [option]
    //      width       unsignedByte    module width (PDF417, QR Code, GS1 DataBar) [option]
    //      height      unsignedByte    module height (PDF417) [option]
    //      size        unsignedShort   the number of columns (PDF417), maximum width (GS1 DataBar) [option]
    // Return:          object          ePOSBuilder object
    // Throws:          object          invalid parameter
    //
    ePOSBuilder.prototype.addSymbol = function (data, type, level, width, height, size) {
        // create empty string
        var s = '';
        // check parameter
        s += getEnumAttr('type', type, regexSymbol);
        // check parameter (option)
        if (level !== undefined) {
            s += getEnumAttr('level', level, regexLevel);
        }
        // check parameter (option)
        if (width !== undefined) {
            s += getUByteAttr('width', width);
        }
        // check parameter (option)
        if (height !== undefined) {
            s += getUByteAttr('height', height);
        }
        // check parameter (option)
        if (size !== undefined) {
            s += getUShortAttr('size', size);
        }
        // append element
        this.message += '<symbol' + s + '>' + escapeText(encodeXmlEntity(data)) + '</symbol>';
        // return builder object
        return this;
    }

    //
    // Function: addCommand method
    // Description: append the XML element to send commands
    // Parameters:
    //      data    string      commands
    // Return:      object      ePOSBuilder object
    //
    ePOSBuilder.prototype.addCommand = function (data) {
        // append element
        this.message += '<command>' + encodeHexBinary(data) + '</command>';
        // return builder object
        return this;
    }

    //
    // Function: addHLine method
    // Description: append the XML element to draw horizontal line
    // Parameters:
    //      x1      unsignedShort   X start position
    //      x2      unsignedShort   X end position
    //      style   string          the style of line (LINE_* constants) [option]
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addHLine = function (x1, x2, style) {
        // create empty string
        var s = '';
        // check parameter
        s += getUShortAttr('x1', x1);
        // check parameter
        s += getUShortAttr('x2', x2);
        // check parameter (option)
        if (style !== undefined) {
            s += getEnumAttr('style', style, regexLine);
        }
        // append element
        this.message += '<hline' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addVLineBegin method
    // Description: append the XML element to draw vertical line
    // Parameters:
    //      x       unsignedShort   X start position
    //      style   string          the style of line (LINE_* constants) [option]
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addVLineBegin = function (x, style) {
        // create empty string
        var s = '';
        // check parameter
        s += getUShortAttr('x', x);
        // check parameter (option)
        if (style !== undefined) {
            s += getEnumAttr('style', style, regexLine);
        }
        // append element
        this.message += '<vline-begin' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addVLineEnd method
    // Description: append the XML element to draw vertical line
    // Parameters:
    //      x       unsignedShort   X end position
    //      style   string          the style of line (LINE_* constants) [option]
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addVLineEnd = function (x, style) {
        // create empty string
        var s = '';
        // check parameter
        s += getUShortAttr('x', x);
        // check parameter (option)
        if (style !== undefined) {
            s += getEnumAttr('style', style, regexLine);
        }
        // append element
        this.message += '<vline-end' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addPageBegin method
    // Description: append the XML element to select page mode
    // Parameters:  none
    // Return:      object      ePOSBuilder object
    //
    ePOSBuilder.prototype.addPageBegin = function () {
        // append element
        this.message += '<page>';
        // return builder object
        return this;
    }

    //
    // Function: addPageEnd method
    // Description: append the XML element to print and return to standard mode (in page mode)
    // Parameters:  none
    // Return:      object      ePOSBuilder object
    //
    ePOSBuilder.prototype.addPageEnd = function () {
        // append element
        this.message += '</page>';
        // return builder object
        return this;
    }

    //
    // Function: addPageArea method
    // Description: append the XML element to set print area in page mode
    // Parameters:
    //      x           unsignedShort   horizontal logical origin
    //      y           unsignedShort   vertical logical origin
    //      width       unsignedShort   print area width
    //      height      unsignedShort   print area height
    // Return:          object          ePOSBuilder object
    // Throws:          object          invalid parameter
    //
    ePOSBuilder.prototype.addPageArea = function (x, y, width, height) {
        // create empty string
        var s = '';
        // check parameter
        s += getUShortAttr('x', x);
        // check parameter
        s += getUShortAttr('y', y);
        // check parameter
        s += getUShortAttr('width', width);
        // check parameter
        s += getUShortAttr('height', height);
        // append element
        this.message += '<area' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addPageDirection method
    // Description: append the XML element to select print direction in page mode
    // Parameters:
    //      dir     string      direction (DIRECTION_* constants)
    // Return:      object      ePOSBuilder object
    // Throws:      object      invalid parameter
    //
    ePOSBuilder.prototype.addPageDirection = function (dir) {
        // create empty string
        var s = '';
        // check parameter
        s += getEnumAttr('dir', dir, regexDirection);
        // append element
        this.message += '<direction' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addPagePosition method
    // Description: append the XML element to set absolute print position in page mode
    // Parameters:
    //      x       unsignedShort   horizontal position
    //      y       unsignedShort   vertical position
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addPagePosition = function (x, y) {
        // create empty string
        var s = '';
        // check parameter
        s += getUShortAttr('x', x);
        // check parameter
        s += getUShortAttr('y', y);
        // append element
        this.message += '<position' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addPageLine method
    // Description: append the XML element to draw line in page mode
    // Parameters:
    //      x1      unsignedShort   X start position
    //      y1      unsignedShort   Y start position
    //      x2      unsignedShort   X end position
    //      y2      unsignedShort   Y end position
    //      style   string          the style of line (LINE_* constants) [option]
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addPageLine = function (x1, y1, x2, y2, style) {
        // create empty string
        var s = '';
        // check parameter
        s += getUShortAttr('x1', x1);
        // check parameter
        s += getUShortAttr('y1', y1);
        // check parameter
        s += getUShortAttr('x2', x2);
        // check parameter
        s += getUShortAttr('y2', y2);
        // check parameter (option)
        if (style !== undefined) {
            s += getEnumAttr('style', style, regexLine);
        }
        // append element
        this.message += '<line' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addPageRectangle method
    // Description: append the XML element to draw rectangle in page mode
    // Parameters:
    //      x1      unsignedShort   X start position
    //      y1      unsignedShort   Y start position
    //      x2      unsignedShort   X end position
    //      y2      unsignedShort   Y end position
    //      style   string          the style of line (LINE_* constants) [option]
    // Return:      object          ePOSBuilder object
    // Throws:      object          invalid parameter
    //
    ePOSBuilder.prototype.addPageRectangle = function (x1, y1, x2, y2, style) {
        // create empty string
        var s = '';
        // check parameter
        s += getUShortAttr('x1', x1);
        // check parameter
        s += getUShortAttr('y1', y1);
        // check parameter
        s += getUShortAttr('x2', x2);
        // check parameter
        s += getUShortAttr('y2', y2);
        // check parameter (option)
        if (style !== undefined) {
            s += getEnumAttr('style', style, regexLine);
        }
        // append element
        this.message += '<rectangle' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addCut method
    // Description: append the XML element to cut paper
    // Parameters:
    //      type    string      cut mode (CUT_* constants) [option]
    // Return:      object      ePOSBuilder object
    // Throws:      object      invalid parameter
    //
    ePOSBuilder.prototype.addCut = function (type) {
        // create empty string
        var s = '';
        // check parameter (option)
        if (type !== undefined) {
            s += getEnumAttr('type', type, regexCut);
        }
        // append element
        this.message += '<cut' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addPulse method
    // Description: append the XML element to generate pulse
    // Parameters:
    //      drawer      string      drawer kick-out connector pin (DRAWER_* constants) [option]
    //      time        string      the pulse on/off time [option]
    // Return:          object      ePOSBuilder object
    // Throws:          object      invalid parameter
    //
    ePOSBuilder.prototype.addPulse = function (drawer, time) {
        // create empty string
        var s = '';
        // check parameter (option)
        if (drawer !== undefined) {
            s += getEnumAttr('drawer', drawer, regexDrawer);
        }
        // check parameter (option)
        if (time !== undefined) {
            s += getEnumAttr('time', time, regexPulse);
        }
        // append element
        this.message += '<pulse' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Function: addSound method
    // Description: append the XML element to sound buzzer
    // Parameters:
    //      pattern     string          a pattern (PATTERN_* constants) [option]
    //      repeat      unsignedByte    the number of times [option]
    // Return:          object          ePOSBuilder object
    // Throws:          object          invalid parameter
    //
    ePOSBuilder.prototype.addSound = function (pattern, repeat) {
        // create empty string
        var s = '';
        // check parameter (option)
        if (pattern !== undefined) {
            s += getEnumAttr('pattern', pattern, regexPattern);
        }
        // check parameter (option)
        if (repeat !== undefined) {
            s += getUByteAttr('repeat', repeat);
        }
        // append element
        this.message += '<sound' + s + '/>';
        // return builder object
        return this;
    }

    //
    // Method: toString
    // Description: get the ePOS-Print XML message
    // Parameters:  none
    // Return:      string      XML message
    //
    ePOSBuilder.prototype.toString = function () {
        // append root element
        var epos = '<epos-print xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print">' +
            this.message + '</epos-print>';
        // return message
        return epos;
    }

    //
    // Function: encodeHexBinary method
    // Description: encode binary data to hex binary data
    // Parameters:
    //      s       string      binary data
    // Return:      string      hex binary data
    //
    function encodeHexBinary(s) {
        var r = '';
        for (i = 0; i < s.length; i++) {
            r += ('0' + s.charCodeAt(i).toString(16)).slice(-2);
        }
        return r;
    }

    //
    // Function: encodeBase64Binary method
    // Description: encode binary data to base64 binary data
    // Parameters:
    //      s       string      binary data
    // Return:      string      base64 binary data
    //
    function encodeBase64Binary(s) {
        var r = '';
        var l = s.length;
        var t = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
        s += '\x00\x00';
        for (var i = 0; i < l; i += 3) {
            var n = (s.charCodeAt(i) << 16) | (s.charCodeAt(i + 1) << 8) | s.charCodeAt(i + 2);
            r += t.charAt((n >> 18) & 63) + t.charAt((n >> 12) & 63) + t.charAt((n >> 6) & 63) + t.charAt(n & 63);
        }
        var p = (3 - l % 3) % 3;
        return r.slice(0, r.length - p) + '=='.slice(0, p);
    }

    //
    // Function: encodeRasterImage method
    // Description: encode image data to raster bit image data
    // Parameters:
    //      data    byte[]      RGBA image data
    //      w       int         image width
    //      h       int         image height
    // Return:      string      raster bit image data
    //
    function encodeRasterImage(data, w, h) {
        var d8 = [
            [0, 32, 8, 40, 2, 34, 10, 42],
            [48, 16, 56, 24, 50, 18, 58, 26],
    	    [12, 44, 4, 36, 14, 46, 6, 38],
            [60, 28, 52, 20, 62, 30, 54, 22],
	        [3, 35, 11, 43, 1, 33, 9, 41],
            [51, 19, 59, 27, 49, 17, 57, 25],
            [15, 47, 7, 39, 13, 45, 5, 37],
            [63, 31, 55, 23, 61, 29, 53, 21]
        ];
        var s = '', n = 0, p = 0;
        for (var y = 0; y < h; y++) {
            for (var x = 0; x < w; x++) {
                var r = data[p++], g = data[p++], b = data[p++], a = data[p++];
                var v = 255 - a + ((r * 29891 + g * 58661 + b * 11448) * a + 12750000) / 25500000;
                var d = (d8[y & 7][x & 7] << 2) + 2;
                if (v < d) {
                    n |= 0x80 >> (x & 7);
                }
                if ((x & 7) == 7 || x == w - 1) {
                    s += String.fromCharCode(n == 16 ? 32 : n);
                    n = 0;
                }
            }
        }
        return s;
    }

    //
    // Function: encodeXmlEntity method
    // Description: encode markup character to XML entity
    // Parameters:
    //      s       string      text data
    // Return:      string      text data with XML entity
    //
    function encodeXmlEntity(s) {
        var markup = /[<>&'"\t\n\r]/g;
        if (markup.test(s)) {
            s = s.replace(markup, function (c) {
                var r = '';
                switch (c) {
                    case '<':
                        r = '&lt;';
                        break;
                    case '>':
                        r = '&gt;';
                        break;
                    case '&':
                        r = '&amp;';
                        break;
                    case "'":
                        r = '&apos;';
                        break;
                    case '"':
                        r = '&quot;';
                        break;
                    case '\t':
                        r = '&#9;';
                        break;
                    case '\n':
                        r = '&#10;';
                        break;
                    case '\r':
                        r = '&#13;';
                        break;
                    default:
                        break;
                }
                return r;
            });
        }
        return s;
    }

    //
    // Function: escapeText method
    // Description: escape sequence for bar code and symbol
    // Parameters:
    //      s       string      text data
    // Return:      string      text data with escape sequence
    //
    function escapeText(s) {
        var escape = /[\\\x00-\x1f\x7f-\xff]/g;
        if (escape.test(s)) {
            s = s.replace(escape, function (c) {
                return (c == '\\') ? '\\\\' : '\\x' + ('0' + c.charCodeAt(0).toString(16)).slice(-2);
            });
        }
        return s;
    }

    //
    // Function: regular expressions
    // Description: enumeration check pattern
    //
    var regexFont = /^(font_[abc]|special_[ab])$/;
    var regexAlign = /^(left|center|right)$/;
    var regexColor = /^(none|color_[1-4])$/;
    var regexBarcode = /^(upc_[ae]|[ej]an13|[ej]an8|code(39|93|128)|itf|codabar|gs1_128|gs1_databar_(omnidirectional|truncated|limited|expanded))$/;
    var regexHri = /^(none|above|below|both)$/;
    var regexSymbol = /^(pdf417_(standard|truncated)|qrcode_model_[12]|maxicode_mode_[2-6]|gs1_databar_(stacked(_omnidirectional)?|expanded_stacked))$/;
    var regexLevel = /^(level_[0-8lmqh]|default)$/;
    var regexLine = /^(thin|medium|thick)(_double)?$/;
    var regexDirection = /^(left_to_right|bottom_to_top|right_to_left|top_to_bottom)$/;
    var regexCut = /^(no_feed|feed|reserve)$/;
    var regexDrawer = /^(drawer_1|drawer_2)$/;
    var regexPulse = /^pulse_[1-5]00$/;
    var regexPattern = /^(none|pattern_[a-e]|error|paper_end)$/;

    //
    // Function: getEnumAttr method
    // Description: get a XML attribute from a parameter (enumration)
    // Parameters:
    //      name    string      parameter name
    //      value   string      parameter value
    //      regex   regex       check pattern
    // Return:      string      XML attribute (' name="value"')
    // Throws:      object      invalid parameter
    //
    function getEnumAttr(name, value, regex) {
        if (!regex.test(value)) {
            throw new Error('Parameter "' + name + '" is invalid');
        }
        return ' ' + name + '="' + value + '"';
    }

    //
    // Function: getBoolAttr method
    // Description: get a XML attribute from a parameter (boolean)
    // Parameters:
    //      name    string      parameter name
    //      value   boolean     parameter value
    // Return:      string      XML attribute (' name="value"')
    //
    function getBoolAttr(name, value) {
        return ' ' + name + '="' + !!value + '"';
    }

    //
    // Function: getIntAttr method
    // Description: get a XML attribute from a parameter (integer)
    // Parameters:
    //      name    string      parameter name
    //      value   integer     parameter value
    //      min     integer     minumum value
    //      max     integer     maximum value
    // Return:      string      XML attribute (' name="value"')
    // Throws:      object      invalid parameter
    //
    function getIntAttr(name, value, min, max) {
        if (isNaN(value) || value < min || value > max) {
            throw new Error('Parameter "' + name + '" is invalid');
        }
        return ' ' + name + '="' + value + '"';
    }

    //
    // Function: getUByteAttr method
    // Description: get a XML attribute from a parameter (unsigned byte)
    // Parameters:
    //      name    string      parameter name
    //      value   integer     parameter value
    // Return:      string      XML attribute (' name="value"')
    // Throws:      object      invalid parameter
    //
    function getUByteAttr(name, value) {
        return getIntAttr(name, value, 0, 255);
    }

    //
    // Function: getUShortAttr method
    // Description: get a XML attribute from a parameter (unsigned short)
    // Parameters:
    //      name    string      parameter name
    //      value   integer     parameter value
    // Return:      string      XML attribute (' name="value"')
    // Throws:      object      invalid parameter
    //
    function getUShortAttr(name, value) {
        return getIntAttr(name, value, 0, 65535);
    }

    //
    // Function: ePOSPrint constructor
    // Description: initialize an ePOS-Print object
    // Parameters:  none
    // Return:      none
    //
    function ePOSPrint() {
        // events
        this.onreceive = null;
        this.onerror = null;
        // constants
        this.ASB_NO_RESPONSE = 0x00000001;
        this.ASB_PRINT_SUCCESS = 0x00000002;
        this.ASB_DRAWER_KICK = 0x00000004;
        this.ASB_OFF_LINE = 0x00000008;
        this.ASB_COVER_OPEN = 0x00000020;
        this.ASB_PAPER_FEED = 0x00000040;
        this.ASB_WAIT_ON_LINE = 0x00000100;
        this.ASB_PANEL_SWITCH = 0x00000200;
        this.ASB_MECHANICAL_ERR = 0x00000400;
        this.ASB_AUTOCUTTER_ERR = 0x00000800;
        this.ASB_UNRECOVER_ERR = 0x00002000;
        this.ASB_AUTORECOVER_ERR = 0x00004000;
        this.ASB_RECEIPT_NEAR_END = 0x00020000;
        this.ASB_RECEIPT_END = 0x00080000;
        this.ASB_BUZZER = 0x01000000;
        this.ASB_SPOOLER_IS_STOPPED = 0x80000000;
    }

    //
    // Function: ePOSprint send method
    // Description: send the ePOS-Print XML message
    // Parameters:
    //      address     string      the address of ePOS-Print service
    //      request     string      request message
    // Return:          none
    // Throws:          object      the browser does not equip XMLHttpRequest
    //
    ePOSPrint.prototype.send = function (address, request) {
        // create SOAP envelope
        var soap = '<?xml version="1.0" encoding="utf-8"?>' +
            '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body>' +
            request + '</s:Body></s:Envelope>';
        // create XMLHttpRequest object
        var xhr = createXMLHttpRequest();
        xhr.open('POST', address, true);
        // set headers
        xhr.setRequestHeader('Content-Type', 'text/xml; charset=UTF-8');
        xhr.setRequestHeader('If-Modified-Since', 'Thu, 01 Jan 1970 00:00:00 GMT');
        xhr.setRequestHeader('SOAPAction', '""');
        // receive event
        var epos = this;
        xhr.onreadystatechange = function () {
            // receive response message
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    fireReceiveEvent(epos, xhr);
                }
                else {
                    fireErrorEvent(epos, xhr);
                }
            }
        }
        // send request message
        xhr.send(soap);
    }


	/*
	Function: createXMLHttpRequest method
	Description: create an XMLHttpRequest object
	Parameters:  none
	Return:      object      XMLHttpRequest object
	Throws:      object      the browser does not equip XMLHttpRequest
    */

	function createXMLHttpRequest()
	{
		var xhr = null;
		if (window.XMLHttpRequest)
		{
			xhr = new XMLHttpRequest();
		}
		else if (window.ActiveXObject)
		{
			xhr = new ActiveXObject('Msxml2.XMLHTTP');
		}
		else
		{
			throw new Error('XMLHttpRequest is not supported');
		}
		return xhr;
	}


    //
    // Function: fireReceiveEvent method
    // Description: generate the onreceive event
    // Parameters:
    //      epos    object      ePOSPrint object
    //      xhr     object      XMLHttpRequest object
    // Return:      none
    //
    function fireReceiveEvent(epos, xhr) {
        if (epos.onreceive) {
            var res = xhr.responseXML.getElementsByTagName('response');
            if (res.length > 0) {
                // fire onreceive event
                epos.onreceive({
                    success: /^(1|true)$/.test(res[0].getAttribute('success')),
                    code: res[0].getAttribute('code'),
                    status: parseInt(res[0].getAttribute('status'))
                });
            }
            else {
                fireErrorEvent(epos, xhr);
            }
        }
    }

    //
    // Function: fireErrorEvent method
    // Description: generate the onerror event
    // Parameters:
    //      epos    object      ePOSPrint object
    //      xhr     object      XMLHttpRequest object
    // Return:      none
    //
    function fireErrorEvent(epos, xhr) {
        // fire onerror event
        if (epos.onerror) {
            epos.onerror({
                status: xhr.status,
                responseText: xhr.responseText
            });
        }
    }


// F I S C A L --- F I S C A L --- F I S C A L --- F I S C A L --- F I S C A L --- F I S C A L --- F I S C A L --- F I S C A L


	/*
	Function: fiscalPrint constructor
	Description: initialize a fiscalPrint object
	Parameters:  none
	Return:      none
	*/

	function fiscalPrint()
	{
		// events
		this.onreceive = null;
		this.onerror = null;

		// constants
		this.ASB_NO_RESPONSE = 0x00000001;
		this.ASB_PRINT_SUCCESS = 0x00000002;
		this.ASB_DRAWER_KICK = 0x00000004;
		this.ASB_OFF_LINE = 0x00000008;
		this.ASB_COVER_OPEN = 0x00000020;
		this.ASB_PAPER_FEED = 0x00000040;
		this.ASB_WAIT_ON_LINE = 0x00000100;
		this.ASB_PANEL_SWITCH = 0x00000200;
		this.ASB_MECHANICAL_ERR = 0x00000400;
		this.ASB_AUTOCUTTER_ERR = 0x00000800;
		this.ASB_UNRECOVER_ERR = 0x00002000;
		this.ASB_AUTORECOVER_ERR = 0x00004000;
		this.ASB_RECEIPT_NEAR_END = 0x00020000;
		this.ASB_RECEIPT_END = 0x00080000;
		this.ASB_BUZZER = 0x01000000;
		this.ASB_SPOOLER_IS_STOPPED = 0x80000000;
	}


	/*
	Function: fiscalPrint send method
	Description: send the fiscal ePOS-Print XML message
	Parameters:
		address		string		The address where fpmate.cgi resides
		request		string		Request message
	Return:			none
	Throws:			object		The browser does not equip XMLHttpRequest
	*/

	fiscalPrint.prototype.send = function (address, request, timeout, callMode)
	{
		timeout = timeout || 0;
		callMode = callMode || "async";

		// create SOAP envelope
		var soap = '<?xml version="1.0" encoding="utf-8"?>\n' +
			'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">\n' +
			'<s:Body>\n' +
			request +
			'</s:Body>\n' +
            '</s:Envelope>\n';
		// create XMLHttpRequest object
		var xhr = createXMLHttpRequest();
		if (callMode == "async")
		{
			xhr.open('POST', address, true);
		}
		else
		{
			xhr.open('POST', address, false); // PHIL false = sincrono
		}
		// set headers
		xhr.setRequestHeader('Content-Type', 'text/xml; charset=UTF-8');
		xhr.setRequestHeader('If-Modified-Since', 'Thu, 01 Jan 1970 00:00:00 GMT');
		xhr.setRequestHeader('SOAPAction', '""');
		// receive event
		var epos = this;

		// PHIL timeout non va con le richieste sincrone
		if (callMode == "async")
		{
			xhr.timeout = timeout;
			xhr.ontimeout = function () {
			console.log("Timed out!!!");
			fireFiscalErrorEvent(epos, xhr);
			}
		}

		xhr.onreadystatechange = function ()
		{
			// receive response message
			// alert("xhr.readyState = " + xhr.readyState + "\n" + "xhr.status = " + xhr.status);
			if (xhr.readyState == 4)
			{
				if (xhr.status == 200)
				{
					fireFiscalReceiveEvent(epos, xhr);
				}
				else
				{
					fireFiscalErrorEvent(epos, xhr);
				}
			}
		}

		// send request message
		xhr.send(soap);
	}

	/*
	Function: fireFiscalReceiveEvent method
	Description: generate the onreceive event
	Parameters:
		epos	object		ePOSPrint object
		xhr		object		XMLHttpRequest object
	Return:		none
	*/

	function fireFiscalReceiveEvent(epos, xhr)
	{
		if (epos.onreceive)
		{
			// alert ("xhr.responseXML.xml = " + xhr.responseXML.xml);
			var res = xhr.responseXML.getElementsByTagName('response');
			if (res.length > 0)
			{
				// fire onreceive event
				var result =
				{
					success: /^(1|true)$/.test(res[0].getAttribute('success')),
					code: res[0].getAttribute('code'),
					status: parseInt(res[0].getAttribute('status'), 10),
					statusText: res[0].getAttribute('status')
				};

				// look for additional info
				var res_add = res[0].getElementsByTagName('addInfo');
				if (res_add.length > 0)
				{
					var list = res_add[0].getElementsByTagName('elementList');
					var list_len = list.length;
					var tag_names_list = list[0].childNodes[0].nodeValue;
					var tag_names_array = tag_names_list.split(',');
					var add_info = {};

					for (var tnai = 0; tnai < tag_names_array.length; tnai++)
					{
						var node = res_add[0].getElementsByTagName(tag_names_array[tnai])[0];
						var node_child = node.childNodes[0];
						var node_val = "";
						// 21/02/2018 Philip Barnett. Alcuni comandi tornano con responseData vuoto. Senza la verifica, possono vericarsi i null Exception.
						// Questa riga non ha risolto il problema - if(node_child.nodeValue != null && node_child.nodeValue != "")
						try
						{
							node_val = node_child.nodeValue;
						}
						catch(err) // Blank lines generate exceptions
						{
							// node_val = "Elemento " + node.childNodes[0] + " vuoto";
						}
						add_info[tag_names_array[tnai]] = node_val;
					}
				}
				else {
					var tag_names_array = "";
					var add_info = "";
				}

				epos.onreceive(result, tag_names_array, add_info, res_add)
			}
			else // res.length <= 0
			{
				// alert ("res.length = " + res.length);
			} // end if (res.length > 0)
		} // end if (epos.onreceive)
	} // end function fireFiscalReceiveEvent(epos, xhr)


	/*
	Function: fireFiscalErrorEvent method
	Description: generate the onerror event
	Parameters:
		epos    object      ePOSPrint object
		xhr     object      XMLHttpRequest object
	Return:      none
	*/

	function fireFiscalErrorEvent(epos, xhr)
	{
		// fire onerror event
		// alert("Error event called");
		if (epos.onerror)
		{
			var result =
				{
					success: 'false',
					code: "FP_NO_ANSWER_NETWORK",
					status: 0,
					responseXML: xhr.responseXML,
					responseText: xhr.responseText
				};

				epos.onerror(result)
		}
	}


    //
    // Function: CanvasPrint constructor
    // Description: initialize a Canvas-Print object
    // Parameters:  none
    // Return:      none
    //

    function CanvasPrint() {
    }
    // inherit from ePOSPrint object
    CanvasPrint.prototype = new ePOSPrint();
    CanvasPrint.prototype.constructor = CanvasPrint;

    //
    // Function: print method
    // Description: print the HTML 5 Canvas
    // Parameters:
    //      address     string      the address of ePOS-Print service
    //      canvas      object      HTML 5 Canvas object
    //      cut         boolean     when true, cut paper [option]
    // Return:          none
    // Throws:          object      the browser does not equip Canvas
    //
    CanvasPrint.prototype.print = function (address, canvas, cut) {
        // check parameter
        if (!canvas.getContext) {
            throw new Error('Canvas is not supported');
        }
        // get HTML 5 Canvas
        var context = canvas.getContext('2d');
        var width = canvas.getAttribute('width');
        var height = canvas.getAttribute('height');
        // create ePOS-Print XML message
        var builder = new ePOSBuilder();
        builder.addImage(context, 0, 0, width, height);
        if (cut) {
            builder.addCut(builder.CUT_FEED);
        }
        // send request message
        this.send(address, builder.toString());
    };


	/*
	Function: epson object
	Description: append constructors to window object
	*/

	// Core module 'pos_epson_printer' appends constructors to the same window object so
	// this implementation avoid to override the epson object.
	if (!window.epson) {
	    window.epson = {}
	}
	window.epson.ePOSBuilder = window.epson.ePOSBuilder || ePOSBuilder
	window.epson.ePOSPrint = window.epson.ePOSPrint || ePOSPrint
	window.epson.CanvasPrint = window.epson.CanvasPrint || CanvasPrint
	window.epson.fiscalPrint = fiscalPrint
	window.epson.encodeBase64Binary = encodeBase64Binary


})(window);


/*
Function:	decodeFpStatus
Description:	Decodes the five printer status bytes
Parameters:	add_info.fpstatus
Return:		printer, ej, receipt, cash_drawer and mode
*/


/*
function decodeFpStatus(add_info.fpStatus)
{

	var printer = "";
	var ej = "";
	var cash_drawer = "";
	var receipt = "";
	var mode = "";

	switch(add_info.fpStatus.substring(0,1)) {
		case "0":
			printer = "OK";
			break;
		case "2":
			printer = "Carta in esaurimento";
			break;
		case "3":
			printer = "Offline (fine carta o coperchio aperto)";
			break;
		default:
			printer = "Risposta errata";
	}

	switch(add_info.fpStatus.substring(1,2)) {
		case "0":
			ej = "OK";
			break;
		case "1":
			ej = "Prossimo ad Esaurimento";
			break;
		case "2":
			ej = "Da formattare";
			break;
		case "3":
			ej = "Precedente";
			break;
		case "4":
			ej = "Di altro misuratore";
			break;
		case "5":
			ej = "Esaurito";
			break;
		default:
			ej = "Risposta errata";
	}

	switch(add_info.fpStatus.substring(2,3)) {
		case "0":
			cash_drawer = "Aperto";
			break;
		case "1":
			cash_drawer = "Chiuso";
			break;
		default:
			cash_drawer = "Risposta errata";
	}

	switch(add_info.fpStatus.substring(3,4)) {
		case "0":
			receipt = "Fiscale aperto";
			break;
		case "1":
			receipt = "Fiscale/Non fiscale chiuso";
			break;
		case "2":
			receipt = "Non fiscale aperto";
			break;
		case "3":
			receipt = "Pagamento in corso";
			break;
		case "4":
			receipt = "Errore ultimo comando ESC/POS con Fiscale/Non fiscale chiuso";
			break;
		case "5":
			receipt = "Scontrino in negativo";
			break;
		case "6":
			receipt = "Errore ultimo comando ESC/POS con Non fiscale aperto";
			break;
		case "7":
			receipt = "Attesa chiusura scontrino modalit&agrave; JAVAPOS";
			break;
		case "8":
			receipt = "Documento fiscale aperto";
			break;
		case "A":
			receipt = "Titolo aperto";
			break;
		case "2":
			receipt = "Titolo chiuso";
			break;
		default:
			receipt = "Risposta errata";
	}

	switch(add_info.fpStatus.substring(4,5)) {
		case "0":
			mode = "Stato registrazione";
			break;
		case "1":
			mode = "Stato X";
			break;
		case "2":
			mode = "Stato Z";
			break;
		case "3":
			mode = "Stato Set";
			break;
		default:
			mode = "Risposta errata";
	}
}
*/
