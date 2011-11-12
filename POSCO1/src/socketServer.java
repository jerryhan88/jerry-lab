

import java.net.ServerSocket;

import java.net.Socket;
import java.util.Vector;

public class socketServer {
	ServerSocket ss;
	Socket s;
	Vector v;

	public socketServer() {
		v = new Vector(5, 5);
		System.out.println("������ ���۵Ǿ����ϴ�.");
	}

	public void giveAndTake() {
		try {
			ss = new ServerSocket(5420);
			ss.getReuseAddress();
			while (true) {
				s = ss.accept();
				ServerSocketThread svrth = new ServerSocketThread(this, s);
				addClient(svrth);
				svrth.start();
			}
		} catch (Exception ee) {
			ee.printStackTrace();
		}

	}

	public void addClient(Thread tr) {
		v.addElement(tr);
		System.out.println("Client 1�� ����, �� " + v.size() + "��");
	}

	public void removeClient(Thread tr) {
		v.removeElement(tr);
		System.out.println("Client 1�� ����, �� " + v.size() + "��");
	}

	public void broadCasting(String sbc) {
		for(int i = 0 ; i < v.size(); i++) {
			ServerSocketThread svtr = (ServerSocketThread)v.elementAt(i);
			svtr.sendMessage(sbc);
		}
	}

}
