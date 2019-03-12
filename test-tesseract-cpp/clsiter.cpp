#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

int main() {

    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    // Initialize tesseract-ocr with English, without specifying tessdata path
    if (api->Init(NULL, "eng")) {
        fprintf(stderr, "Could not initialize tesseract.\n");
        exit(1);
    }

    // Open input image with leptonica library
    Pix *image = pixRead("../test.png");
    api->SetImage(image);
    api->SetVariable("save_blob_choices", "T");
    //api->SetRectangle(37, 228, 548, 31);
    api->Recognize(NULL);

    tesseract::ResultIterator* ri = api->GetIterator();
    tesseract::PageIteratorLevel level = tesseract::RIL_SYMBOL;
    if (ri != 0) {
        do {
            const char* symbol = ri->GetUTF8Text(level);
            float conf = ri->Confidence(level);
            if (symbol != 0) {
                printf("symbol %s, conf: %f", symbol, conf);
                bool indent = false;
                tesseract::ChoiceIterator ci(*ri);
                do {
                    if (indent) printf("\t\t ");
                    printf("\t- ");
                    const char* choice = ci.GetUTF8Text();
                    printf("%s conf: %f\n", choice, ci.Confidence());
                    indent = true;
                } while (ci.Next());
            }
            printf("---------------------------------------------\n");
            delete[] symbol;
        } while ((ri->Next(level)));
    }
    // Destroy used object and release memory
    api->End();
    pixDestroy(&image);

    return 0;
}


