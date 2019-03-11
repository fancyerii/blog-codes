package com.github.fancyerii.test.pdfbox;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.encryption.InvalidPasswordException;
import org.apache.pdfbox.rendering.ImageType;
import org.apache.pdfbox.rendering.PDFRenderer;
import org.apache.pdfbox.tools.imageio.ImageIOUtil;

public class ConvertTest {

	public static void main(String[] args) throws InvalidPasswordException, IOException {
		PDDocument document = PDDocument.load(new File("/home/lili/data/testen.pdf"));
		PDFRenderer pdfRenderer = new PDFRenderer(document);
		for (int page = 0; page < document.getNumberOfPages(); ++page) {
			if(page>0 && page %100==0) {
				System.out.println("page: "+page);
			}
//			float w=document.getPage(page).getMediaBox().getWidth();
//			float h=document.getPage(page).getMediaBox().getHeight();
//			System.out.println(String.format("w: %f, h: %f",w, h));
			BufferedImage bim = pdfRenderer.renderImageWithDPI(page, 300, ImageType.RGB);
			//BufferedImage bim = pdfRenderer.renderImage(page, 2.0f);
			
			// suffix in filename will be used as the file format
			ImageIOUtil.writeImage(bim, "/home/lili/data/testen-" + (page + 1) + ".png", 300);
		}
	}

}
