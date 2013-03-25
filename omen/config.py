import knewton.config

OmenConfigPath = knewton.config.ConfigPathDefaults([
	'', '~/.omen', '/etc/omen'])
OmenConfig = knewton.config.ConfigDefault(config_path=OmenConfigPath)

def get_config(name):
	OmenConfig.fetch_config(name)

