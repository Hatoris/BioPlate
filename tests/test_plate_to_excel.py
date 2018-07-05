import unittest
import contextlib
import numpy as np

from pathlib import Path, PurePath
from pyexcel_xlsx import get_data
from BioPlate import BioPlate
from BioPlate.writer.to_excel import BioPlateToExcel
from BioPlate.database.plate_db import PlateDB
from BioPlate.database.plate_historic_db import PlateHist
from string import ascii_uppercase
from tabulate import tabulate


def remove_tail(liste):
    lis = liste[::-1]
    for i, val in enumerate(lis):
        if not val:
            del lis[i]
            liste = lis[::-1]
            return remove_tail(liste)
        else:
            return liste


def remove_np_tail(liste):
    lis = liste[::-1]
    isempty = np.vectorize(any)
    for i, val in enumerate(lis):
        if val.any():
            del lis[i]
            liste = lis[::-1]
            return remove_np_tail(liste)
        else:
            return liste


def like_read_excel(plate, header=True, lst=None):
    rm_empty = [] if lst is None else lst
    if plate.name == "Plate":
        return clean_list(rm_empty, plate, header=header)
    elif plate.name == "Inserts":
        n = 0
        for parts in plate:
            parts = parts if header else parts[1:, 1:]
            u = len(parts)
            for part in parts:
                if header:
                    if n == 0:
                        part[0] = "TOP"
                    elif u == n:
                        part[0] = "BOT"
                if u == n:
                    rm_empty.append([])
                clean_list(rm_empty, part, parts=True)
                n += 1
        return rm_empty


def like_read_excel_stack(stack, header=True):
    ll = None
    for plate in stack:
        if ll is None:
            ll = like_read_excel(plate, header=header, lst=None)
        else:
            ll = like_read_excel(plate, header=header, lst=ll)
        ll.append([])
    del ll[-1]
    return ll


def clean_list(li, plate, parts=False, header=True):
    if not parts:
        plate = plate if header else plate[1:, 1:]
        for x in plate:
            li.append(remove_tail(list(x)))
    else:
        li.append(remove_tail(list(plate)))
    return li


def as_read_excel(PTE, action, plate, filename, sheetname, conditions=None):
    if conditions:
        for attr, value in conditions.items():
            setattr(PTE, attr, value)
    getattr(PTE, action)(plate)
    getattr(PTE, "close")()
    return get_data(filename)[sheetname]


def like_read_data(plate, accumulate=True, order="C", header=None, stack=False):
    rm_empty = list(
        map(list, getattr(plate, "iterate")(accumulate=accumulate, order=order))
    )
    if header is not None:
        pass
    else:
        val = len(rm_empty[0])
        if plate.name == "Plate":
            header = ["well", "value0"]
        elif plate.name == "Inserts":
            if accumulate:
                header = ["well", "top0", "bot0"]
            else:
                header = ["well", "top", "bot"]
        if val <= 2:
            pass
        else:
            if plate.name == "Inserts":
                pass
            #                if val <= 3:
            #                    for i in range(1, val):
            #                        header.append('top' + str(i))
            #                        header.append('bot' + str(i))
            elif plate.name == "BioPlate":
                for i in range(1, val):
                    header.append("value" + str(i))
    if not stack:
        rm_empty.insert(0, header)
    return list(map(remove_tail, rm_empty))


def like_read_data_stack(stack, accumulate=True, order="C", header=None):
    if stack[0].name == "Plate":
        if accumulate:
            header = ["well", "value0"]
        else:
            header = ["well", "value"]
    elif stack[0].name == "Inserts":
        if accumulate:
            header = ["well", "top0", "bot0"]
        else:
            header = ["well", "top", "bot"]
    if accumulate:
        for i in range(1, len(stack)):
            if stack[0].name == "Inserts":
                header.append("top" + str(i))
                header.append("bot" + str(i))
            else:
                header.append("value" + str(i))
    rm_empty = list(
        map(list, getattr(stack, "iterate")(accumulate=accumulate, order=order))
    )
    rm_empty.insert(0, header)
    return list(map(remove_tail, rm_empty))


def like_read_count(plate, empty="empty", Inserts=False):
    val = list(plate.count().items())
    if isinstance(val[0][1], dict):
        nv = []
        for pos, valdict in val:
            valdict = list(map(list, valdict.items()))
            addp = lambda x: [pos] + x
            nv += list(map(addp, valdict))
        val = nv
        if isinstance(val[0][2], dict):
            nv = []
            for i in range(len(val)):
                num, pos, valdict = val[i]
                valdict = list(map(list, valdict.items()))
                addp = lambda x: [num, pos] + x
                nv += list(map(addp, valdict))
            val = nv
    val = list(map(list, val))
    change = lambda x: empty if x == "" else x
    val = list(map(lambda y: list(map(change, y)), val))
    len_header = len(val[0])
    if len_header == 2:
        hd = ["infos", "count"]
    elif len_header == 3:
        if not Inserts:
            hd = ["plate", "infos", "count"]
        else:
            hd = ["position", "infos", "count"]
    elif len_header == 4:
        hd = ["plate", "position", "infos", "count"]
    val.insert(0, hd)
    return val


def nested_dict_to_list(dd):
    local_list = []
    for key, value in dd.items():
        local_list.append(key)
        local_list.extend(nested_dict_to_list(value))
    return local_list


class TestPlateToExcel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This function is run one time at the beginning of tests
        :return:
        """
        cls.pdb = PlateDB(db_name="test_plate.db")
        cls.pdb.add_plate(
            numWell=96,
            numColumns=12,
            numRows=8,
            surfWell=0.29,
            maxVolWell=200,
            workVolWell=200,
            refURL="https://csmedia2.corning.com/LifeSciences/Media/pdf/cc_surface_areas.pdf",
        )

    @classmethod
    def tearDownClass(cls):
        """
        This function is run one time at the end of tests
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path(
                PurePath(
                    Path(__file__).parent.parent
                    / "BioPlate/database/DBFiles"
                    / "test_plate.db"
                )
            ).unlink()
            Path(
                PurePath(
                    Path(__file__).parent.parent
                    / "BioPlate/database/DBFiles"
                    / "test_plate_historic.db"
                )
            ).unlink()
            Path(
                PurePath(
                    Path(__file__).parent.parent
                    / "BioPlate/database/DBFiles"
                    / "test_plate_to_excel.xlsx"
                )
            ).unlink()

    def setUp(self):
        """
        This function is run every time at the beginning of each test
        :return:
        """
        self.PTE = BioPlateToExcel("test.xlsx")
        v = {
            "A[2,8]": "VC",
            "H[2,8]": "MS",
            "1-4[B,G]": ["MLR", "NT", "1.1", "1.2"],
            "E-G[8,10]": ["Val1", "Val2", "Val3"],
        }
        v1 = {
            "A[2,8]": "VC1",
            "H[2,8]": "MS1",
            "1-4[B,G]": ["MLR1", "NT1", "1.3", "1.4"],
            "E-G[8,10]": ["Val4", "Val5", "Val6"],
        }
        v2 = {
            "A[2,8]": "Top",
            "H[2,8]": "MS",
            "1-4[B,G]": ["MLR", "NT", "1.1", "1.2"],
            "E-G[8,10]": ["Val1", "Val2", "Val3"],
        }
        v3 = {
            "A[2,8]": "Bot",
            "H[2,8]": "MS1",
            "1-4[B,G]": ["MLR1", "NT1", "1.3", "1.4"],
            "E-G[8,10]": ["Val4", "Val5", "Val6"],
        }
        self.plt = BioPlate({"id": 1}, db_name="test_plate.db")
        self.plt.set(v)
        self.plt1 = BioPlate(12, 8)
        self.plt1.set(v1)
        self.stack = self.plt + self.plt1
        self.Inserts = BioPlate(12, 8, inserts=True)
        self.Inserts.top.set(v)
        self.Inserts.bot.set(v3)
        self.Inserts1 = BioPlate(12, 8, inserts=True)
        self.Inserts1.bot.set(v1)
        self.Inserts1.top.set(v2)
        self.stacki = self.Inserts + self.Inserts1

    def tearDown(self):
        """
        This function is run every time at the end of each test
        :return:
        """
        with contextlib.suppress(FileNotFoundError):
            Path(PurePath("test.xlsx")).unlink()

    ###TEST DATA SHEET
    def test_representation_BioPlate(self):
        read_excel = as_read_excel(
            self.PTE, "representation", self.plt, "test.xlsx", "plate_representation"
        )
        rm_empty = like_read_excel(self.plt)
        self.assertEqual(read_excel, rm_empty)

    def test_representation_BioPlate_hd(self):
        c = {"header": False}
        read_excel = as_read_excel(
            self.PTE,
            "representation",
            self.plt,
            "test.xlsx",
            "plate_representation",
            conditions=c,
        )
        rm_empty = like_read_excel(self.plt, header=False)
        self.assertEqual(read_excel, rm_empty)

    def test_representation_BioPlateInserts(self):
        read_excel = as_read_excel(
            self.PTE,
            "representation",
            self.Inserts,
            "test.xlsx",
            "plate_representation",
        )
        rm_empty = like_read_excel(self.Inserts)
        self.assertEqual(read_excel, rm_empty)

    def test_representation_BioPlateInserts_hd(self):
        c = {"header": False}
        read_excel = as_read_excel(
            self.PTE,
            "representation",
            self.Inserts,
            "test.xlsx",
            "plate_representation",
            conditions=c,
        )
        rm_empty = like_read_excel(self.Inserts, header=False)
        self.assertEqual(read_excel, rm_empty)

    def test_representation_BioPlateStack_bp(self):
        read_excel = as_read_excel(
            self.PTE, "representation", self.stack, "test.xlsx", "plate_representation"
        )
        rm_empty = like_read_excel_stack(self.stack)
        self.assertEqual(read_excel, rm_empty)

    def test_representation_BioPlateStack_bp_hd(self):
        c = {"header": False}
        read_excel = as_read_excel(
            self.PTE,
            "representation",
            self.stack,
            "test.xlsx",
            "plate_representation",
            conditions=c,
        )
        rm_empty = like_read_excel_stack(self.stack, header=False)
        self.assertEqual(read_excel, rm_empty)

    def test_representation_BioPlateStack_bpi(self):
        read_excel = as_read_excel(
            self.PTE, "representation", self.stacki, "test.xlsx", "plate_representation"
        )
        rm_empty = like_read_excel_stack(self.stacki)
        self.assertEqual(read_excel, rm_empty)

    def test_representation_BioPlateStack_bpi_hd(self):
        c = {"header": False}
        read_excel = as_read_excel(
            self.PTE,
            "representation",
            self.stacki,
            "test.xlsx",
            "plate_representation",
            conditions=c,
        )
        rm_empty = like_read_excel_stack(self.stacki, header=False)
        self.assertEqual(read_excel, rm_empty)

    ###TEST DATA SHEET
    def test_data_BioPlate(self):
        c = None
        read_excel = as_read_excel(
            self.PTE, "data", self.plt, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data(self.plt)
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlate_row(self):
        c = {"order": "R"}
        read_excel = as_read_excel(
            self.PTE, "data", self.plt, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data(self.plt, order="R")
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlateInserts(self):
        c = None
        read_excel = as_read_excel(
            self.PTE, "data", self.Inserts, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data(self.Inserts)
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlateInserts_row(self):
        c = {"order": "R"}
        read_excel = as_read_excel(
            self.PTE, "data", self.Inserts, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data(self.Inserts, order="R")
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlateInserts_row_acc(self):
        c = {"order": "R", "accumulate": False}
        read_excel = as_read_excel(
            self.PTE, "data", self.Inserts, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data(self.Inserts, order="R", accumulate=False)
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlateStack_bp(self):
        c = None
        read_excel = as_read_excel(
            self.PTE, "data", self.stack, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data_stack(self.stack)
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlateStack_bp_row(self):
        c = {"order": "R"}
        read_excel = as_read_excel(
            self.PTE, "data", self.stack, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data_stack(self.stack, order="R")
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlateStack_bp_row_acc(self):
        c = {"order": "R", "accumulate": False}
        read_excel = as_read_excel(
            self.PTE, "data", self.stack, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data_stack(self.stack, order="R", accumulate=False)
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlateStack_bpi(self):
        c = None
        read_excel = as_read_excel(
            self.PTE, "data", self.stacki, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data_stack(self.stacki)
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlateStack_bpi_row(self):
        c = {"order": "R"}
        read_excel = as_read_excel(
            self.PTE, "data", self.stacki, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data_stack(self.stacki, order="R")
        self.assertEqual(read_excel, rm_empty)

    def test_data_BioPlateStack_bpi_row_acc(self):
        c = {"order": "R", "accumulate": False}
        read_excel = as_read_excel(
            self.PTE, "data", self.stacki, "test.xlsx", "plate_data", conditions=c
        )
        rm_empty = like_read_data_stack(self.stacki, order="R", accumulate=False)
        self.assertEqual(read_excel, rm_empty)

    ###TEST COUNT SHEET
    def test_count_BioPlate(self):
        c = None
        read_excel = as_read_excel(
            self.PTE, "count", self.plt, "test.xlsx", "plate_count", conditions=c
        )
        rm_empty = like_read_count(self.plt)
        self.assertEqual(read_excel, rm_empty)

    def test_count_BioPlate_emp(self):
        c = {"empty": "vide"}
        read_excel = as_read_excel(
            self.PTE, "count", self.plt, "test.xlsx", "plate_count", conditions=c
        )
        rm_empty = like_read_count(self.plt, empty="vide")
        self.assertEqual(read_excel, rm_empty)

    def test_count_BioPlateInserts(self):
        c = None
        read_excel = as_read_excel(
            self.PTE, "count", self.Inserts, "test.xlsx", "plate_count", conditions=c
        )
        rm_empty = like_read_count(self.Inserts, Inserts=True)
        self.assertEqual(read_excel, rm_empty)

    def test_count_BioPlateInserts(self):
        c = {"empty": "vide"}
        read_excel = as_read_excel(
            self.PTE, "count", self.Inserts, "test.xlsx", "plate_count", conditions=c
        )
        rm_empty = like_read_count(self.Inserts, empty="vide", Inserts=True)
        self.assertEqual(read_excel, rm_empty)

    def test_count_BioPlateStack_bp(self):
        c = None
        read_excel = as_read_excel(
            self.PTE, "count", self.stack, "test.xlsx", "plate_count", conditions=c
        )
        rm_empty = like_read_count(self.stack)
        self.assertEqual(read_excel, rm_empty)

    def test_count_BioPlateStack_bp_em(self):
        c = {"empty": "vide"}
        read_excel = as_read_excel(
            self.PTE, "count", self.stack, "test.xlsx", "plate_count", conditions=c
        )
        rm_empty = like_read_count(self.stack, empty="vide")
        self.assertEqual(read_excel, rm_empty)

    def test_count_BioPlateStack_bpi(self):
        c = None
        read_excel = as_read_excel(
            self.PTE, "count", self.stacki, "test.xlsx", "plate_count", conditions=c
        )
        rm_empty = like_read_count(self.stacki, Inserts=True)
        self.assertEqual(read_excel, rm_empty)

    def test_count_BioPlateStack_bpi_em(self):
        c = {"empty": "vide"}
        read_excel = as_read_excel(
            self.PTE, "count", self.stacki, "test.xlsx", "plate_count", conditions=c
        )
        rm_empty = like_read_count(self.stacki, empty="vide", Inserts=True)
        self.assertEqual(read_excel, rm_empty)


    def test_error_init(self):
        with self.assertRaises(ValueError):
            BioPlateToExcel("test.xlsx", sheets = ["bob",], test=True)
        with self.assertRaises(Exception):
            BioPlateToExcel("test.xlsx", sheets = "bob")

    def test_in_memory(self):
        t = BioPlateToExcel("test.xlsx", test=True)
        self.assertEqual(t.get_test(), b'')
        x = BioPlateToExcel("test.xlsx")
        self.assertEqual(x.get_test(), None)

if __name__ == "__main__":
    unittest.main()
