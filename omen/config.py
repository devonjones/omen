import k.config

OmenConfigPath = k.config.ConfigPathDefaults([
	'', '~/.omen', '/etc/omen'])
OmenConfig = k.config.ConfigDefault(config_path=OmenConfigPath)

