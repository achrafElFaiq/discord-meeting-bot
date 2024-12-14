const { Client, GatewayIntentBits, Partials } = require('discord.js');
const { joinVoiceChannel, getVoiceConnection, VoiceConnectionStatus, AudioReceiver } = require('@discordjs/voice');
const fs = require('fs');
const { PassThrough } = require('stream');
const { opus } = require('@discordjs/opus');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildVoiceStates,
  ],
  partials: [Partials.Channel],
});

client.once('ready', () => {
  console.log(`✅ Bot is online as ${client.user.tag}`);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  // Join voice channel command
  if (message.content === '!join') {
    if (message.member.voice.channel) {
      try {
        const connection = joinVoiceChannel({
          channelId: message.member.voice.channel.id,
          guildId: message.guild.id,
          adapterCreator: message.guild.voiceAdapterCreator,
        });

        message.channel.send('🎉 I have joined the voice channel!');

        // Ensure the connection is established
        if (connection) {
          console.log('✅ Connection established to the voice channel.');

          // Set the bot as deafened if needed (optional)
          const botMember = message.guild.members.cache.get(client.user.id);
          if (botMember) {
            await botMember.voice.setDeaf(false);  // Deafening the bot
            console.log('Bot has been deafened.');
          } else {
            console.error('❌ Could not find the bot member in the guild.');
          }

          // Start receiving audio streams
          connection.on(VoiceConnectionStatus.Ready, async () => {
            console.log('Voice connection is ready to receive audio.');

            const receiver = connection.receiver;

            // Listen for incoming audio from members
            connection.on('userSpeaking', (user, speaking) => {
              if (speaking) {
                console.log(`🎤 ${user.tag} is speaking`);

                // Subscribe to the user's audio stream
                const audioStream = receiver.subscribe(user.id, {
                  end: { behavior: 'manual' }, // Ensure manual stream end
                });

                // Create a writable stream to save audio
                const outputFile = fs.createWriteStream('audio/meeting_audio.pcm');
                audioStream.pipe(outputFile);

                audioStream.on('end', () => {
                  console.log('Audio stream ended.');
                });

                audioStream.on('error', (err) => {
                  console.error('Error in audio stream:', err);
                });
              }
            });
          });
        } else {
          console.error('❌ Failed to establish voice connection.');
          message.channel.send('❌ I could not join the voice channel.');
        }

      } catch (error) {
        console.error('❌ Error joining voice channel:', error);
        message.channel.send('❌ I could not join the voice channel.');
      }
    } else {
      message.channel.send('❌ You need to be in a voice channel first!');
    }
  }

  // Leave voice channel command
  if (message.content === '!leave') {
    const connection = getVoiceConnection(message.guild.id);
    if (connection) {
      connection.destroy();
      message.channel.send('👋 I have left the voice channel!');
    } else {
      message.channel.send('❌ I am not in a voice channel.');
    }
  }

  // Test command
  if (message.content === '!hello') {
    message.channel.send('👋 Hello! I am here and ready to record meetings.');
  }
});

// Log the bot in using the token
client.login(process.env.TOKEN);
