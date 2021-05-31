import csv
import datetime


class Books():
    def __init__(self):
        self.books = {}

    def add_book(self, row):
        book = Book(row=row)

        if not book.isbn_issn:
            print(f'No ISBN/ISSN for {book}')
            return

        self.books[book.isbn_issn] = book

    def get_book(self, name):
        book = self.books.get(name)

        return book

    def __iter__(self):
        for key in self.books.keys():
            book = self.books.get(key)

            yield book

    def __repr__(self):
        return f'{len(self.books.keys())} books'


class Book():
    def __init__(self, row=None):
        self.loans = 0
        self.latest_loan = None

        if row:
            self.from_csv_row(row)

    def add_loan(self, row):
        self.loans = self.loans + 1

        loan_date = row.get('Lainauspvm')

        if not self.latest_loan or loan_date > self.latest_loan:
            self.latest_loan = loan_date

    def from_csv_row(self, row):
        self.classification = row.get('Hyllypaikka')
        self.location = row.get('Sijainti')
        self.demografic = row.get('Osasto')
        self.Publish_date = row.get('Julkaisuvuosi')
        self.language = row.get('Kieli')
        self.material = row.get('Aineistolaji')
        self.publish_type = row.get('Julkaisutyyppi')
        self.isbn_issn = row.get('ISBN/ISSN')
        self.name = row.get('Nimeke')
        self.author = row.get('Tekijä')
        self.signum = row.get('Signum')

    def to_csv_row(self):
        return [
            self.classification,
            self.location,
            self.demografic,
            self.Publish_date,
            self.language,
            self.material,
            self.publish_type,
            self.isbn_issn,
            self.name,
            self.author,
            self.signum,
            self.loans,
            self.latest_loan
        ]

    def __repr__(self):
        return f'<Book("{self.name}" by {self.author}   {self.publish_type} {self.isbn_issn})'


def main():
    books = Books()

    # Read in the csv file containing all individual books
    # Check for missing isbn numbers and for duplicates
    # Convert csv row into a book and add to book list

    with open('data/kaikki_nimekkeet.csv', 'r') as input_file:
        reader = csv.DictReader(input_file)

        unknown = []
        duplicates = []

        for row in reader:
            isbn = row.get('ISBN/ISSN')

            if not isbn:
                print(f'Book {row.get("Nimeke")} has no ISBN/ISSN')
                unknown.append(row)
                continue

            if books.get_book(isbn):
                print(f'Book {row.get("Nimeke")} has a duplicate')
                duplicates.append(row)
                continue

            books.add_book(row)

        print(f'{books}')
        print(f'{len(unknown)} books missing ISBN/ISSN')
        print(f'{len(duplicates)} duplicate books')

    # Read in a csv file containing all loan transactions
    # Check for missing isbn numbers or dates
    # Increment loan number for book and change latest loan date if need be

    with open('data/kaikki_lainat.csv', 'r') as input_file:
        reader = csv.DictReader(input_file)

        unknown = []
        missing_isbn = []
        missing_date = []
        total = 0

        for row in reader:
            total = total + 1

            isbn = row.get('ISBN/ISSN')

            if not isbn:
                print('No ISBN/ISSN associated with loan')
                missing_isbn.append(row)
                continue

            loan_date = row.get('Lainauspvm')

            if not loan_date:
                print('No date associated with loan')
                missing_date.append(row)
                continue

            loan_date = datetime.datetime.strptime(loan_date, "%Y%m%d")

            row['Lainauspvm'] = loan_date

            book = books.get_book(isbn)

            if not book:
                print(f'No book found with ISBN/ISSN {isbn}')
                unknown.append(row)
                continue

            book.add_loan(row)

        print(f'{total} total loans')
        print(f'{len(missing_isbn)} loans with no ISBN/ISSN')
        print(f'{len(missing_date)} loans with no date')
        print(f'{len(unknown)} loans with unknown ISBN/ISSN')

    # Write books into a csv file with their loan amounts and the latest loan date

    with open('output.csv', 'w+') as output_file:

        headers = [
            "Hyllypaikka",
            "Sijainti",
            "Osasto",
            "Julkaisuvuosi",
            "Kieli",
            "Aineistolaji",
            "Julkaisutyyppi",
            "isbn/issn",
            "Nimeke",
            "Tekijä",
            "Signum",
            "Lainat",
            "Viimeksi Lainattu"
        ]

        writer = csv.writer(output_file)

        writer.writerow(headers)

        for book in books:
            row = book.to_csv_row()

            writer.writerow(row)


if __name__ == '__main__':
    main()
