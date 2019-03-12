package com.github.fancyerii.test.tesseract;

import static org.bytedeco.javacpp.lept.pixDestroy;
import static org.bytedeco.javacpp.lept.pixRead;

import org.bytedeco.javacpp.BytePointer;
import org.bytedeco.javacpp.PointerPointer;
import org.bytedeco.javacpp.tesseract;
import org.bytedeco.javacpp.lept.BOX;
import org.bytedeco.javacpp.lept.BOXA;
import org.bytedeco.javacpp.lept.PIX;
import org.bytedeco.javacpp.tesseract.TessBaseAPI;

public class GetComponent {

	public static void main(String[] args) {

		TessBaseAPI api = new TessBaseAPI();
		// Initialize tesseract-ocr with English, without specifying tessdata path
		if (api.Init(null, "eng") != 0) {
			System.err.println("Could not initialize tesseract.");
			System.exit(1);
		}

		// Open input image with leptonica library
		PIX image = pixRead(args.length > 0 ? args[0] : "testen-1.png");
		api.SetImage(image);
		// Get OCR result
		// Boxa* boxes = api->GetComponentImages(tesseract::RIL_TEXTLINE, true, NULL,
		// NULL);
		// printf("Found %d textline image components.\n", boxes->n);
		// for (int i = 0; i < boxes->n; i++) {
		// BOX* box = boxaGetBox(boxes, i, L_CLONE);
		// api->SetRectangle(box->x, box->y, box->w, box->h);
		// char* ocrResult = api->GetUTF8Text();
		// int conf = api->MeanTextConf();
		// fprintf(stdout, "Box[%d]: x=%d, y=%d, w=%d, h=%d, confidence: %d, text: %s",
		// i, box->x, box->y, box->w, box->h, conf, ocrResult);
		// }
		BOXA boxes = api.GetComponentImages(tesseract.RIL_TEXTLINE, true, (PointerPointer) null, null);
		System.out.print(String.format("Found %d textline image components.\n", boxes.n()));
		for (int i = 0; i < boxes.n(); i++) {
			BOX box = boxes.box(i);
			api.SetRectangle(box.x(), box.y(), box.w(), box.h());
			BytePointer text = api.GetUTF8Text();
			int conf = api.MeanTextConf();
			System.out.println(String.format("Box[%d]: x=%d, y=%d, w=%d, h=%d, confidence: %d, text: %s", i, box.x(),
					box.y(), box.w(), box.h(), conf, text.getString()));
			text.deallocate();
		}
		// Destroy used object and release memory
		api.End();
		pixDestroy(image);
	}

}
