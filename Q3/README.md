  # Relatório Jogo da Velha P2P
 
 # Funcionamento do servidor:
 1. Servidor aguarda por mensagem com a string 'Get Game'.
 2. Ao receber a mensagem, servidor guarda em uma fila o endereço do remetente da mensagem.
 3. Quando a fila tem 2 endereços (jogadores), envia o endereço do 1° da fila para o 2° e o endereço do 2° para o 1°. 
 Removendo os 2 da fila em seguida.
 
 # Funcionamento do jogador:
 1. Jogador abre a interface gráfica e cria a classe Player, que se encarrega do socket e da lógica do jogo.
 2. O socket é criado, e envia a requisição 'Get Game' ao servidor.
 3. Aguarda até que o servidor envie o endereço de um adversário, junto com a decisão entre 'X' ou 'O'.
 4. Ao receber um endereço, envia uma confirmação de conexão ao adversário, e aguarda pela confirmação dele.
 Caso a confirmação do adversário não chegue em 10 segundos, é enviada uma nova requisição ao servidor.
 5. Ao receber a confirmação do jogador adversário, o jogo é iniciado, com o jogador 'X' iniciando e o jogador 'O' esperando sua vez.
 6. Quando está em seu turno, o seu processo envia mensagens 'Connected' para o adversário a cada 5 segundos, confirmando que
 a conexão continua estabelecida. Caso o adversário (que está aguardando a sua jogada) não receba nenhuma confirmação em 20 segundos,
 indica que a conexão foi perdida, e fecha o programa.
 6. Quando está aguardando o turno do adversário, o processo espera por mensagens 'Connected' para confirmar a conexão e continuar esperando
 a jogada do adversário. Caso se passe 20 segundos, o programa é encerrado, como descrito acima. Também, caso não chegue nenhuma confirmação
 em 10 segundos, a sua jogada anterior é reenviada, pois há chance de que ela tenha se perdido na rede e o adversário ainda esteja esperando
 por ela.
 
 obs.1: As leituras no buffer do socket são não bloqueantes. Isso indica que somente será realizada leitura quando houver dados no buffer.
 Caso contrário, o processo segue o fluxo.
 obs.2: A função __myTurn serve apenas para enviar a mensagem 'Connected' (confirmação de conexão), sendo a função sendPlay responsável por
 enviar ao adversário a sua jogada quando o jogador clica no botão em sua vez.

# How to run
TODO