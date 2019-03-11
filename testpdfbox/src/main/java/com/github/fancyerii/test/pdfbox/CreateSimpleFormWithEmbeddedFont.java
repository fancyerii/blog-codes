package com.github.fancyerii.test.pdfbox;

import java.io.IOException;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDResources;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.font.PDFont;
import org.apache.pdfbox.pdmodel.font.PDType0Font;
import org.apache.pdfbox.pdmodel.interactive.annotation.PDAnnotationWidget;
import org.apache.pdfbox.pdmodel.interactive.form.PDAcroForm;
import org.apache.pdfbox.pdmodel.interactive.form.PDTextField;

public class CreateSimpleFormWithEmbeddedFont {
	private CreateSimpleFormWithEmbeddedFont() {
	}

	public static void main(String[] args) throws IOException {
		// Create a new document with an empty page.
		try (PDDocument doc = new PDDocument()) {
			PDPage page = new PDPage();
			doc.addPage(page);
			PDAcroForm acroForm = new PDAcroForm(doc);
			doc.getDocumentCatalog().setAcroForm(acroForm);

			// Note that the font is fully embedded. If you use a different font, make sure
			// that
			// its license allows full embedding.
			PDFont formFont = PDType0Font.load(doc, CreateSimpleFormWithEmbeddedFont.class
					.getResourceAsStream("/simhei.ttf"), false);

			// Add and set the resources and default appearance at the form level
			final PDResources resources = new PDResources();
			acroForm.setDefaultResources(resources);
			final String fontName = resources.add(formFont).getName();

			// Acrobat sets the font size on the form level to be
			// auto sized as default. This is done by setting the font size to '0'
			acroForm.setDefaultResources(resources);
			String defaultAppearanceString = "/" + fontName + " 0 Tf 0 g";

			PDTextField textBox = new PDTextField(acroForm);
			textBox.setPartialName("SampleField");
			textBox.setDefaultAppearance(defaultAppearanceString);
			acroForm.getFields().add(textBox);

			// Specify the widget annotation associated with the field
			PDAnnotationWidget widget = textBox.getWidgets().get(0);
			PDRectangle rect = new PDRectangle(50, 700, 200, 50);
			widget.setRectangle(rect);
			widget.setPage(page);
			page.getAnnotations().add(widget);

			// set the field value. Note that the last character is a turkish capital I with
			// a dot,
			// which is not part of WinAnsiEncoding
			textBox.setValue("Sample field 陌");

			doc.save("/home/lili/data/SimpleFormWithEmbeddedFont.pdf");
		}
	}
}
