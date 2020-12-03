package com.github.fancyerii.wechatdriver;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;

public class ImageTools {
    private static final int BACKGROUND_R = 204;
    private static final int BACKGROUND_G = 204;
    private static final int BACKGROUND_B = 204;
    private static final double THRESHOLD = 0.8;

    public static boolean isQRCodeImage(byte[] bytes) throws IOException {
        InputStream is = new ByteArrayInputStream(bytes);
        BufferedImage image = ImageIO.read(is);
        int width = image.getWidth();
        int height = image.getHeight();
        int bgCount = 0;
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                int color = image.getRGB(col, row);
                int r = (color >> 16) & 0xFF;
                int g = (color >> 8) & 0xFF;
                int b = (color >> 0) & 0xFF;
                if (r == BACKGROUND_R && g == BACKGROUND_G && b == BACKGROUND_B) {
                    bgCount++;
                }
            }
        }
        if (1.0 * bgCount / (width * height) > THRESHOLD) {
            return false;
        } else {
            return true;
        }
    }
}
