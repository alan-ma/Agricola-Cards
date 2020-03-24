from fpdf import FPDF
import os


# measurements in mm
CARD_HEIGHT = 92
SPACING = 0
HORIZONTAL_SPACING = 59
MARGIN = 10


class PDF(FPDF):
    # Page footer
    def footer(self):
        # Position at 1.5cm from bottom
        self.set_y(-15)
        # Courier 8
        self.set_font('Courier', '', 8)
        # Page number
        text = self.title + ' - Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, text, 0, 0, 'C')


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    total = 0
    for deck in os.listdir('images'):
        # Landscape, pt units, Letter
        pdf = PDF('L', 'mm', 'Letter')
        pdf.alias_nb_pages()
        pdf.set_title(deck)
        pdf.set_font('Courier', '', 10)

        images = os.listdir('images/%s' % deck)
        images = [image for image in images if image[-4:] == '.jpg']
        total += len(images)
        print("%d cards in deck %s" % (len(images), deck))
        for chunk in chunks(images, 8):
            pdf.add_page()
            for i, image in enumerate(chunk[:4]):
                path = 'images/%s/%s' % (deck, image)
                pdf.image(
                    path,
                    x=HORIZONTAL_SPACING * i + MARGIN,
                    y=MARGIN,
                    h=CARD_HEIGHT,
                )
            for i, image in enumerate(chunk[4:]):
                path = 'images/%s/%s' % (deck, image)
                pdf.image(
                    path,
                    x=HORIZONTAL_SPACING * i + MARGIN,
                    y=CARD_HEIGHT + SPACING + MARGIN,
                    h=CARD_HEIGHT,
                )

        # output to file
        pdf.output('output/%s.pdf' % deck, 'F')
    print("%d total cards" % total)


if __name__ == '__main__':
    main()
