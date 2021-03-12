import saw
from saw.llvm import Contract, void
from saw.llvm_types import i32

import unittest
from pathlib import Path

class Swap(Contract):
    def __init__(self) -> None:
        super().__init__()
        self.ty = i32

    def specification(self) -> None:
        x = self.fresh_var(self.ty, "x")
        y = self.fresh_var(self.ty, "y")
        x_ptr = self.alloc(self.ty, points_to=x)
        y_ptr = self.alloc(self.ty, points_to=y)

        self.execute_func(x_ptr, y_ptr)

        self.points_to(x_ptr, y)
        self.points_to(y_ptr, x)
        self.returns(void)


class SwapEasyTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        saw.connect(reset_server=True)

    @classmethod
    def tearDownClass(self):
        saw.reset_server()
        saw.disconnect()

    def test_swap(self):

        if __name__ == "__main__": saw.view(saw.LogResults())
        swap_bc = str(Path('tests','saw','test-files', 'swap.bc'))

        mod = saw.llvm_load_module(swap_bc)

        result = saw.llvm_verify(mod, 'swap', Swap())
        self.assertIs(result.is_success(), True)


if __name__ == "__main__":
    unittest.main()
