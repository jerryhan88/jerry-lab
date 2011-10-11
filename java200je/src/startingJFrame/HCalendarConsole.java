package startingJFrame;

import java.util.Calendar;
import java.util.GregorianCalendar;

public class HCalendarConsole {
	int year = 2003;
	int month = 8;
	Calendar today;
	Calendar cal;

	public HCalendarConsole() {
		today = Calendar.getInstance();
		cal = new GregorianCalendar();
		calInput();
		calSet();
	}

	public void calInput() {
		InputsInt ins = new InputsInt();

		int[] a = ins.input(2, 0, 3000);

		year = a[0];
		month = a[1];
	}

	public void calSet() {
		cal.set(Calendar.YEAR, year);
		cal.set(Calendar.MONTH, (month - 1));
		cal.set(Calendar.DATE, 1);

		System.out.println(cal.get(Calendar.YEAR) + "³â/"
				+ (cal.get(Calendar.MONTH) + 1) + "¿ù");

		int dayOfWeek = cal.get(Calendar.DAY_OF_WEEK);

		int j = 0, k = 0;
		int hopping = 0;
		System.out.println("Sun\tMon\tTue\tWed\tThu\tFri\tSat");
		for (int i = cal.getFirstDayOfWeek(); i < dayOfWeek; i++) {
			j++;
		}
		hopping = j;
		for (int kk = 0; kk < hopping; kk++) {
			System.out.print("\t");
		}
		for (int i = cal.getMinimum(Calendar.DAY_OF_MONTH); i <= cal
				.getMaximum(Calendar.DAY_OF_MONTH); i++) {
			cal.set(Calendar.DATE, i);
			if (cal.get(Calendar.MONTH) != month - 1) {
				break;
			}

			if (hopping == 0 && ((i - 1) / 7) == 0) {
				System.out.print(i + "\t");
			} else {
				if (cal.get(Calendar.DAY_OF_WEEK) == 1) {
					System.out.println();
				}
			}
			System.out.print(i + "\t");
		}
	}
}
