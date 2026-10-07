import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).parents[1]))
from cost.calculator import compare
class T(unittest.TestCase):
 def test_units(self):self.assertEqual(compare(3,60,.1,60)['gpu_estimate'],.000833)
if __name__=='__main__':unittest.main()
