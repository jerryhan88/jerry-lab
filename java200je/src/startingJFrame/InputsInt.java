package startingJFrame;

public class InputsInt {

	public boolean isDuplicate(int[] da) {
		boolean isD = false;
		for (int i = 0; i < da.length; i++) {
			for (int j = i; j < da.length; j++) {
				if (i != j && da[i] == da[j]) {
					isD = true;
					break;
				}
			}
		}
		return isD;
	}

	public int[] input(int n, int start, int end) {
		int[] num = new int[n];
		int count = 0;
		while (true) {
			try {
				int a = Integer.parseInt(javax.swing.JOptionPane
						.showInputDialog(null, (count + 1) + " 번째 수를 넣으시오"));
				if (a >= start && a <= end) {
					num[count++] = a;
				} else {
					throw new Exception("범위가 잘못되었습니다. \n 다시 입력하시오");
				}
				if (count >= n) {
					break;
				}
			} catch (NumberFormatException ee) {
				javax.swing.JOptionPane.showMessageDialog(null,
						"잘못된 형식으로 입력되었습니다. \n 다시 입력하시오");
			} catch (Exception ee) {
				javax.swing.JOptionPane
						.showMessageDialog(null, ee.getMessage());
			}
		}
		return num;
	}

	public int[] input(int n, int start, int end, boolean b) {
		int[] num = new int[n];
		int count = 0;

		if (b == false) {
			while (true) {
				num = input(n, start, end);
				if (isDuplicate(num)) {
					javax.swing.JOptionPane.showMessageDialog(null,
							"중복되었습니다. \n 다시 입력하시오");
				} else {
					break;
				}
			}
		} else {
			num = input(n, start, end);
		}
		return num;
	}

	public void prints(int[] a) {
		for (int i = 0; i < a.length; i++) {
			System.out.print(a[i] + " ");
		}
	}
}
