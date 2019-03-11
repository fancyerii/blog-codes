package com.github.fancyerii.test.pdfbox;

import java.awt.Dimension;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.encryption.InvalidPasswordException;
import org.apache.pdfbox.rendering.ImageType;
import org.apache.pdfbox.rendering.PDFRenderer;
import org.apache.pdfbox.tools.imageio.ImageIOUtil;

public class ConvertToImages {

	public static void main(String[] args) throws InvalidPasswordException, IOException {
		System.setProperty("sun.java2d.cmm", "sun.java2d.cmm.kcms.KcmsServiceProvider"); 

		String path="/home/lili/下载/books/汪曾祺全集1.pdf";
		String dir="/home/lili/data/wang/book1";
		new File(dir).mkdirs();
		PDDocument document = PDDocument.load(new File(path));
		PDFRenderer pdfRenderer = new PDFRenderer(document);
		for (int page = 0; page < document.getNumberOfPages(); ++page) {
			BufferedImage bim = pdfRenderer.renderImageWithDPI(page, 300, ImageType.RGB);
			ImageIOUtil.writeImage(bim, dir + "/" + (page + 1) + ".png", 300);
		}
		document.close();
	}

}
