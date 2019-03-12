#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

int main() {
    tesseract::Orientation orientation;
    tesseract::WritingDirection direction;
    tesseract::TextlineOrder order;
    float deskew_angle;

    PIX *image = pixRead("../test.png");
    tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();
    api->Init(NULL, "eng");
    api->SetPageSegMode(tesseract::PSM_AUTO_OSD);
    api->SetImage(image);
    api->Recognize(0);

    tesseract::PageIterator* it = api->AnalyseLayout();
    it->Orientation(&orientation, &direction, &order, &deskew_angle);
    printf("Orientation: %d;\nWritingDirection: %d\nTextlineOrder: %d\n" \
         "Deskew angle: %.4f\n",
            orientation, direction, order, deskew_angle);
    api->End();
    pixDestroy(&image);
    
    
    return 0;
}


