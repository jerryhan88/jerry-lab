import java.awt.*;
import java.util.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;

public class Graph extends JComponent implements ActionListener {
	private static final long serialVersionUID = -4160057866273543810L;
	// 목적지를 random하게 지정하기 위해
	Random r = new Random(1);
	// 9개의 block 그리기
	Block[] b = new Block[9];
	// 3개의 ship 그리기
	Ship[] sh = new Ship[3];
	// 가로에 48개, 세로로 27개의 Node를 두고 있음
	Node n[] = new Node[27 * 48];
	// tractor들을 저장하는 Vector 임
	Vector<Tractor> tractorGroup = new Vector<Tractor>();
	// 출발지나 목적지로 가능한 Node들을 저장
	Vector<Node> possibleNode = new Vector<Node>();
	// ShortestPathFinding을 위해
	SPF Spf = new SPF();
	// 타이머 즉, 시뮬레이션의 속도를 조작 함
	final int timerDelay = 1;

	Graph() {
		for (int i = 0; i < b.length; i++) { // Block 9개 그리기
			b[i] = new Block();
			b[i].x = (i % 3) * (240/* Block 가로 */+ 80) + 50;
			b[i].y = (i / 3) * (60/* Block 세로 */+ 40) + 50;
		}
		for (int i = 0; i < sh.length; i++) { // ship 3개 그리기
			sh[i] = new Ship();
			sh[i].x = (i % 3) * (240/* Ship 가로 */+ 80) + 50;
			sh[i].y = 15 + 20 * 36 + 10 - 20 * 3 - 20 * 3 - 20 * 3;
		}

		for (int i = 0; i < n.length; i++) {
			n[i] = new Node(); // Node 그리기
			n[i].x = (i % 48) * (10/* Node 지름 */+ 10/* Edge */) + 30;
			n[i].y = (i / 48) * (10 + 10) + 30;
		}
		// SPF에서 ShortestPathPlan을 위해 Node들을 Vector 안에 다 넣어 둠
		// 겸사겸사 id도 같이 지정해 주면서 다른일들을 수월하게 함
		for (int i = 0; i < n.length; i++) {
			Spf.addNode(n[i]);
			n[i].id = i;
		}
		// 여기서 부터는 Node간의 edge를 이어주는 작업임
		// 먼저 가로부터 시작!
		for (int i = 0; i < n.length; i++) {
			if ((i >= 0 && i < 2 * 48) || (i >= 5 * 48 && i < 7 * 48)
					|| (i >= 10 * 48 && i < 12 * 48)
					|| (i >= 15 * 48 && i < 17 * 48)) {
				if (i % 48 == 47)
					continue;
				// 방향이 west인 부분들
				n[i + 1].addEdge(n[i]);
			}
			if ((i >= 17 * 48 && i < 21 * 48)) {
				if (i % 48 == 47)
					continue;
				// 양 방향임
				n[i + 1].addEdge(n[i]);
				n[i].addEdge(n[i + 1]);
			}

			if (i >= 23 * 48 && i < 27 * 48) {
				if (i % 48 == 47)
					continue;
				// 방향이 east인 Node들
				n[i].addEdge(n[i + 1]);
			}
		}
		for (int i = 2; i < 15; i++) {
			// 가장 가 쪽 부분 or block 사이에 있는 edge들 양방향 연결
			if (i == 5 || i == 6 || i == 10 || i == 11)
				continue;
			n[i * 48].addEdge(n[i * 48 + 1]);
			n[i * 48 + 1].addEdge(n[i * 48]);
			n[i * 48 + 14].addEdge(n[i * 48 + 15]);
			n[i * 48 + 15].addEdge(n[i * 48 + 14]);
			n[i * 48 + 16].addEdge(n[i * 48 + 17]);
			n[i * 48 + 17].addEdge(n[i * 48 + 16]);
			n[i * 48 + 30].addEdge(n[i * 48 + 31]);
			n[i * 48 + 31].addEdge(n[i * 48 + 30]);
			n[i * 48 + 32].addEdge(n[i * 48 + 33]);
			n[i * 48 + 33].addEdge(n[i * 48 + 32]);
			n[i * 48 + 46].addEdge(n[i * 48 + 47]);
			n[i * 48 + 47].addEdge(n[i * 48 + 47]);
		}
		for (int i = 0; i < 47; i++) {
			// QC가 있을 자리 근처에 있는 Node들 양방향 연결
			if (i == 2 || i == 3 || i == 4 || i == 5 || i == 11 || i == 12
					|| i == 13 || i == 14 || i == 15 || i == 22 || i == 23
					|| i == 24 || i == 25 || i == 32 || i == 33 || i == 34
					|| i == 35 || i == 42 || i == 43 || i == 44 || i == 45)
				continue;
			n[48 * 21 + i].addEdge(n[48 * 21 + 1 + i]);
			n[48 * 21 + 1 + i].addEdge(n[48 * 21 + i]);
			n[48 * 22 + i].addEdge(n[48 * 22 + 1 + i]);
			n[48 * 22 + 1 + i].addEdge(n[48 * 22 + i]);
		}

		// 세로 addEdge
		for (int i = 0; i < 15; i++) {
			// 15번째 이내에 있는 Node들 중 아래 또는 윗 방향을 고려한 Node들 예를 들자면
			// 바로 아래의 addEdge 같은 경우 아래로 향하는 방향임
			n[48 * i].addEdge(n[48 * (i + 1)]);
			n[48 * i + 1].addEdge(n[48 * (i + 1) + 1]);
			n[48 * i + 14].addEdge(n[48 * (i + 1) + 14]);
			n[48 * i + 15].addEdge(n[48 * (i + 1) + 15]);
			// 이거 같은 경우 윗 방향임
			n[48 * (i + 1) + 16].addEdge(n[48 * i + 16]);
			n[48 * (i + 1) + 17].addEdge(n[48 * i + 17]);
			n[48 * i + 30].addEdge(n[48 * (i + 1) + 30]);
			n[48 * i + 31].addEdge(n[48 * (i + 1) + 31]);
			n[48 * (i + 1) + 32].addEdge(n[48 * i + 32]);
			n[48 * (i + 1) + 33].addEdge(n[48 * i + 33]);
			n[48 * (i + 1) + 46].addEdge(n[48 * i + 46]);
			n[48 * (i + 1) + 47].addEdge(n[48 * i + 47]);
		}
		for (int i = 0; i < 5; i++) {
			// block과 QC 사이의 상하 양방향 edge들임
			n[48 * (15 + i)].addEdge(n[48 * (16 + i)]);
			n[48 * (15 + i) + 1].addEdge(n[48 * (16 + i) + 1]);
			n[48 * (16 + i) + 46].addEdge(n[48 * (15 + i) + 46]);
			n[48 * (16 + i) + 47].addEdge(n[48 * (15 + i) + 47]);
		}
		for (int i = 2; i < 46; i++) {
			// block의 가쪽 or block 사이의 상하 edge들
			n[i].addEdge(n[i + 48]);
			n[i + 48].addEdge(n[i]);
			n[i + 48 * 5].addEdge(n[i + 48 * 6]);
			n[i + 48 * 6].addEdge(n[i + 48 * 5]);
			n[i + 48 * 10].addEdge(n[i + 48 * 11]);
			n[i + 48 * 11].addEdge(n[i + 48 * 10]);
			n[i + 48 * 15].addEdge(n[i + 48 * 16]);
			n[i + 48 * 16].addEdge(n[i + 48 * 15]);
			n[i + 48 * 16].addEdge(n[i + 48 * 17]);
			n[i + 48 * 17].addEdge(n[i + 48 * 16]);
			n[i + 48 * 17].addEdge(n[i + 48 * 18]);
			n[i + 48 * 18].addEdge(n[i + 48 * 17]);
			n[i + 48 * 18].addEdge(n[i + 48 * 19]);
			n[i + 48 * 19].addEdge(n[i + 48 * 18]);
			n[i + 48 * 19].addEdge(n[i + 48 * 20]);
			n[i + 48 * 20].addEdge(n[i + 48 * 19]);
		}

		for (int i = 48 * 23; i < 48 * 26; i++) {
			// 재일 아랫쪽에 있는 edge들을 상하로 연결 시킴
			n[i].addEdge(n[i + 48]);
			n[i + 48].addEdge(n[i]);
		}

		for (int i = 0; i < 48; i++) {
			// QC가 세워지는 부근의 edge들 상하 연결
			if (i == 3 || i == 4 || i == 5 || i == 12 || i == 13 || i == 14
					|| i == 15 || i == 23 || i == 24 || i == 25 || i == 33
					|| i == 34 || i == 35 || i == 43 || i == 44 || i == 45)
				continue;
			n[i + 48 * 20].addEdge(n[i + 48 * 21]);
			n[i + 48 * 21].addEdge(n[i + 48 * 20]);
			n[i + 48 * 21].addEdge(n[i + 48 * 22]);
			n[i + 48 * 22].addEdge(n[i + 48 * 21]);
			n[i + 48 * 22].addEdge(n[i + 48 * 23]);
			n[i + 48 * 23].addEdge(n[i + 48 * 22]);
		}

		for (int i = 0; i < 11; i++) {
			// block 쪽에서 tractor 들의 목적지가 되는 Node들 저장해 둠
			possibleNode.add(n[48 + 2 + i]);
			possibleNode.add(n[48 + 18 + i]);
			possibleNode.add(n[48 + 34 + i]);
			possibleNode.add(n[48 * 5 + 2 + i]);
			possibleNode.add(n[48 * 5 + 18 + i]);
			possibleNode.add(n[48 * 5 + 34 + i]);
			possibleNode.add(n[48 * 6 + 2 + i]);
			possibleNode.add(n[48 * 6 + 18 + i]);
			possibleNode.add(n[48 * 6 + 34 + i]);
			possibleNode.add(n[48 * 10 + 2 + i]);
			possibleNode.add(n[48 * 10 + 18 + i]);
			possibleNode.add(n[48 * 10 + 34 + i]);
			possibleNode.add(n[48 * 11 + 2 + i]);
			possibleNode.add(n[48 * 11 + 18 + i]);
			possibleNode.add(n[48 * 11 + 34 + i]);
			possibleNode.add(n[48 * 15 + 2 + i]);
			possibleNode.add(n[48 * 15 + 18 + i]);
			possibleNode.add(n[48 * 15 + 34 + i]);
		}
		// 목적지 Node에 방향을 줘야함 (그래야 차들이 정차시키는 방향 또는 출발 방향을 정해 줄 수 있음)
		for (int j = 0; j < possibleNode.size(); j++) {
			possibleNode.get(j).setDirection(Node.destinationState.west);
		}
		// QC 아래에 있는 Node들 주의!! 재일 왼쪽과 오른쪽은 tractor의 방향을 고려하여 빼 주어야 함
		for (int i = 48 * 23; i < 48 * 27; i++) {
			if (i % 48 == 0 || i % 48 == 47)
				continue;
			possibleNode.add(n[i]);
			n[i].setDirection(Node.destinationState.east);
		}
		// tractor 들을 하나씩 추가 시킴
		tractorGroup.add(new Tractor(n[48 * 23 + 6], n[48 * 6 + 24],
				Color.blue, 0));
		tractorGroup.add(new Tractor(n[48 + 23], n[48 * 26 + 18], Color.GREEN,
				1));
		tractorGroup.add(new Tractor(n[48 * 5 + 23], n[48 * 26 + 18 + 3],
				Color.orange, 2));
		tractorGroup.add(new Tractor(n[48 * 11 + 24], n[48 * 26 + 30],
				Color.pink, 3));
		tractorGroup.add(new Tractor(n[48 * 11 + 44], n[48 * 26 + 46],
				Color.magenta, 4));
		tractorGroup.add(new Tractor(n[48 * 24 + 23], n[48 * 5 + 40],
				Color.YELLOW, 5));
		tractorGroup
				.add(new Tractor(n[48 * 25 + 24], n[48 + 2], Color.blue, 6));
		tractorGroup.add(new Tractor(n[48 * 25 + 23], n[48 + 18], Color.GREEN,
				7));
		tractorGroup.add(new Tractor(n[48 * 5 + 40], n[48 * 25 + 18 + 3],
				Color.blue, 8));
		tractorGroup.add(new Tractor(n[48 * 6 + 24], n[48 * 24 + 17],
				Color.pink, 9));
		tractorGroup.add(new Tractor(n[48 * 25 + 2], n[48 * 6 + 6], Color.RED,
				10));
		tractorGroup.add(new Tractor(n[48 * 25 + 30], n[48 + 8], Color.GREEN,
				11));
		tractorGroup.add(new Tractor(n[48 * 26 + 21], n[48 * 10 + 9],
				Color.orange, 12));
		tractorGroup.add(new Tractor(n[48 * 26 + 40], n[48 * 15 + 8],
				Color.pink, 13));
		tractorGroup.add(new Tractor(n[48 * 25 + 3], n[48 * 11 + 24],
				Color.RED, 14));
		tractorGroup.add(new Tractor(n[48 * 26 + 40], n[48 + 40], Color.GREEN,
				15));
		tractorGroup.add(new Tractor(n[48 * 25 + 23], n[48 * 5 + 24],
				Color.orange, 16));
		tractorGroup.add(new Tractor(n[48 * 24 + 34], n[48 * 11 + 42],
				Color.pink, 17));
		tractorGroup.add(new Tractor(n[48 * 10 + 10], n[48 * 24 + 30],
				Color.RED, 18));
		tractorGroup.add(new Tractor(n[48 + 4], n[48 * 24 + 31], Color.magenta,
				19));
		// 시작할때 첫 번째 PathPlanning
		for (int i = 0; i < tractorGroup.size(); i++) {
			Tractor tr = tractorGroup.get(i);
			Node start = tr.start;
			Node end = tr.end;
			Spf.ShortestPathFinding(start, end);
			tr.savePath(start, end);
		}
		// 타이머 달기
		new javax.swing.Timer(timerDelay, this).start();
	}
	// tractor가 현재 있는 위치의 다음번 Node의 상태를 보는 method임
	// tractor가 진행하는 알고리즘에 대해서는 파워포인트 자료에서 찾아 보면 됨
	private void seeNextNode(Tractor t) {
		Node nowNode = t.Path.get(t.Path.size() - 1);
		Node nextNode = t.Path.get(t.Path.size() - 2);

		if (!nextNode.occupied) {
			// 아무것도 없다면 무난히 진행함
			t.state = Tractor.tractorState.move;
		} else {
			// 일단 다음 Node의 tractor를 불러 들임
			Tractor nextNodeTracktor = tractorGroup
					.get(nextNode.nowNodeTracktor.number);

			switch (nextNodeTracktor.state) {
			case move:
				t.state = Tractor.tractorState.wait;
				break;

			case wait:
				Tractor T1 = t;
				Tractor T2 = nextNodeTracktor;
				Node T1NowNode = T1.Path.get(T1.Path.size() - 1);
				Node T1NextNode = T1.Path.get(T1.Path.size() - 2);
				Node T2NowNode = T2.Path.get(T2.Path.size() - 1);
				Node T2NextNode = T2.Path.get(T2.Path.size() - 2);

				if (T1NowNode == T2NextNode && T1NextNode == T2NowNode) {
					T2.tmpCount++;
					if (T1.tmpCount == 1) {
						T1NextNode.special = true;
						Spf.ShortestPathFinding(T1NowNode, T1.end);
						T1NextNode.special = false;

						t.state = Tractor.tractorState.move;
						t.tmpCount = 0;
						if (Spf.success) {
							T1.savePath(T1NowNode, T1.end);
							T1.state = Tractor.tractorState.move;
						} else {
							T1.state = Tractor.tractorState.block;
						}
						break;
					}
					t.state = Tractor.tractorState.wait;
				}
				t.state = Tractor.tractorState.wait;
				break;
			default:
				if (nextNodeTracktor.state == Tractor.tractorState.stop) {
					t.state = Tractor.tractorState.wait;
				} else {
					nextNode.special = true;
					Spf.ShortestPathFinding(nowNode, t.end);
					nextNode.special = false;

					if (Spf.success) {
						t.savePath(nowNode, t.end);
						t.state = Tractor.tractorState.move;
					} else {
						t.state = Tractor.tractorState.block;
					}
				}
				break;
			}
		}
	}

	public void actionPerformed(ActionEvent e) {
		for (int i = 0; i < tractorGroup.size(); i++) {
			Tractor t = tractorGroup.get(i);
			Node nowNode = t.Path.lastElement();

			if (t.Path.size() == 1) {
				t.state = Tractor.tractorState.stop;
			}

			switch (t.state) {
			case stop:
				t.stopTime++;
				if (t.stopTime == 10) {
					t.stopTime = -1;
					Node newStart = t.end;
					Node newTarget = null;

					do {
						int z = r.nextInt(possibleNode.size());
						newTarget = possibleNode.get(z);
					} while (newTarget == newStart);

					Spf.ShortestPathFinding(t.end, newTarget);
					if (Spf.success) {
						t.savePath(newStart, newTarget);
						t.state = Tractor.tractorState.move;
					} else {
						t.state = Tractor.tractorState.block;
						t.saveStartEnd(newStart, newTarget);
						break;
					}
					seeNextNode(t);
				}
				break;

			case block:
				if (t.Path.size() == 1) {
					Spf.ShortestPathFinding(nowNode, t.end);
					if (Spf.success) {
						t.savePath(nowNode, t.end);
						t.state = Tractor.tractorState.move;
					} else {
						t.state = Tractor.tractorState.block;
						break;
					}
				} else {
					Tractor tmpTracktor = t;
					Node nextNode = t.Path.get(t.Path.size() - 2);
					nextNode.special = true;
					Spf.ShortestPathFinding(nowNode, t.end);
					nextNode.special = false;

					if (Spf.success) {
						t.savePath(nowNode, t.end);
						if (t.Path.size() >= tmpTracktor.Path.size()) {
							t = tmpTracktor;
						}
						t.state = Tractor.tractorState.move;
					} else {
						t.state = Tractor.tractorState.block;
						break;
					}
				}
				seeNextNode(t);
				break;

			default:
				seeNextNode(t);
				break;
			}

			if (t.state == Tractor.tractorState.move) {
				Node tmp = nowNode;
				t.Path.get(t.Path.size() - 2).setOccupy(t);
				t.Path.remove(t.Path.size() - 1);
				tmp.setNotOcuupy();
			}
			repaint();
		}
	}
	// 그림을 그리자 ㅎㅎ
	public void paintComponent(Graphics g) {
		// ship쪽에 있는 Line
		g.drawLine(15, 15 + 20 * 36 - 20 * 3 - 20 * 3 - 20 * 3, 15 + 20 * 48,
				15 + 20 * 36 - 20 * 3 - 20 * 3 - 20 * 3);
		for (int i = 0; i < n.length; i++) {
			// QC 근처에 없어야 할 Node들 처리  그리고 나머진 다 그린다
			if (((i >= 48 * 21 + 3 && i <= 48 * 21 + 5)
					|| (i >= 48 * 21 + 12 && i <= 48 * 21 + 15)
					|| (i >= 48 * 21 + 23 && i <= 48 * 21 + 25)
					|| (i >= 48 * 21 + 33 && i <= 48 * 21 + 35) || (i >= 48 * 21 + 43 && i <= 48 * 21 + 45))
					|| ((i >= 48 * 22 + 3 && i <= 48 * 22 + 5)
							|| (i >= 48 * 22 + 12 && i <= 48 * 22 + 15)
							|| (i >= 48 * 22 + 23 && i <= 48 * 22 + 25)
							|| (i >= 48 * 22 + 33 && i <= 48 * 22 + 35) || (i >= 48 * 22 + 43 && i <= 48 * 22 + 45)))
				continue;
			n[i].draw(g);
		}
		for (int i = 0; i < sh.length; i++) {
			sh[i].draw(g);
		}
		for (int i = 0; i < tractorGroup.size(); i++) {
			tractorGroup.get(i).drawPath(g);
		}
		for (int i = 0; i < b.length; i++) {
			b[i].draw(g);
		}
	}

}
