import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

public class Question2mathGUI_4268763_vutomi_mohube{
    static class GuessingGame implements ActionListener{

        private int y;
        private int x;
        private JFrame frame;
        private JLabel label;
        private JPanel panel;
        private JTextField textField;

        public GuessingGame(){
            Random random = new Random();
            y = random.nextInt(10);
            x = random.nextInt(10);

            frame = new JFrame("Guessing Game");

            label = new JLabel(x +" + "+ y +"=");
            label.setHorizontalAlignment(SwingConstants.CENTER);

            textField = new JTextField(1);
            textField.setHorizontalAlignment(SwingConstants.CENTER);

            JButton button = new JButton("Submit");
            button.addActionListener(this);

            panel = new JPanel();
            panel.setBorder(BorderFactory.createEmptyBorder(30, 30, 10, 30));
            panel.setLayout(new GridLayout(0,1));
            panel.add(label);
            panel.add(textField);
            panel.add(button);

            frame.add(panel, BorderLayout.NORTH);
            frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
            frame.pack();
            frame.setVisible(true);
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            int input = Integer.parseInt(textField.getText());
            int counterCorrect = 0;
            int counterWrong = 0;

                    if (input == (x + y)) {
                        counterCorrect++;
                        label.setText("Correct:" + counterCorrect + "Wrong:" + counterWrong);
                    } else if (input < (x + y)) {
                        counterWrong++;
                        label.setText("Correct:" + counterCorrect + "Wrong:" + counterWrong);
                    } else {
                        counterWrong++;
                        label.setText("Correct:" + counterCorrect + "Wrong:" + counterWrong);
                    }


        }


        public static void main(String args[]) {

            GuessingGame gui = new GuessingGame();
        }

    }
}