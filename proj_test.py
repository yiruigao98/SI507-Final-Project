import sqlite3
import unittest

DBNAME = "laptops.db"
class TestLaptopTable(unittest.TestCase):

    def test1(self):
        conn = sqlite3.connect("laptops.db")
        cur = conn.cursor()
        # Test1: test brand and length of the table:
        results = cur.execute("SELECT Brand FROM Laptops")
        brands = results.fetchall()
        self.assertIn(('Apple',), brands)
        self.assertEqual(len(brands), 485)

        # Test2: test size ranges:
        results = cur.execute("SELECT MIN(Size), MAX(Size) FROM Laptops")
        size_range = results.fetchall()
        self.assertEqual(size_range[0][0], 10.0)
        self.assertEqual(size_range[0][1], 17.3)        

        # Test3: test a particular product (name):
        results = cur.execute('''
            SELECT [Name], Size, Price, Color FROM Laptops
            WHERE [Name] LIKE '%MacBook Pro%'
            ORDER BY PRICE DESC
        ''')
        macbookpros = results.fetchall()
        self.assertEqual(len(macbookpros), 63)
        self.assertEqual(macbookpros[0][2], 3799.99)
        self.assertEqual(macbookpros[1][3], "Space Gray")

        # Test4: test a particular product (name):
        results = cur.execute('''
            SELECT [Name], [Memory(GB)], Storage, [Average Rating] FROM Laptops
            WHERE Color LIKE '%gray%' AND Storage LIKE '%256%'
            ORDER BY [Average Rating] DESC
        ''')
        results = results.fetchall()
        self.assertEqual(len(results), 19)
        self.assertEqual(results[0][2], "256GB Solid State Drive")
        self.assertEqual(results[2][0], '15.6" Touch-Screen Laptop')

        conn.close()


class TestReviewTable(unittest.TestCase):

    def test2(self):
        conn = sqlite3.connect("laptops.db")
        cur = conn.cursor()
        # Test1: test length of the table:
        results = cur.execute("SELECT SKU FROM Reviews")
        SKUs = results.fetchall()
        self.assertEqual(len(SKUs), 555)

        # Test2: test number of products that have at least seven or even no reviews:
        results = cur.execute("SELECT [Review 7] FROM Reviews WHERE [Review 7] IS NOT '' ")
        SKUs = results.fetchall()
        self.assertEqual(len(SKUs), 190)
        results = cur.execute("SELECT [Review 1] FROM Reviews WHERE [Review 1] IS NOT '' ")
        SKUs = results.fetchall()
        self.assertEqual(len(SKUs), 302)
        conn.close()


class TestJoinTable(unittest.TestCase):
    
    def test3(self):
        conn = sqlite3.connect("laptops.db")
        cur = conn.cursor()
        # Test1: test number of laptop from Apple that have reviews:
        results = cur.execute('SELECT COUNT(t1.Id) FROM Laptops AS t1 JOIN Reviews AS t2 ON t1.SKU = t2.SKU WHERE t2.[Review 1] IS NOT "" AND t1.Brand = "Apple"')
        results = results.fetchall()
        self.assertEqual(results[0][0], 68)

        # Test2: test number of products that have sizez smaller than 15:
        results = cur.execute('SELECT COUNT(t1.Id) FROM Laptops AS t1 JOIN Reviews AS t2 ON t1.SKU = t2.SKU WHERE t2.[Review 1] IS NOT "" AND t1.Size < 15')
        self.assertEqual(results.fetchall()[0][0], 190)
        conn.close()




unittest.main()