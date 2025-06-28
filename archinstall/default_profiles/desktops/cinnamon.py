from typing import override

from archinstall.default_profiles.profile import GreeterType, ProfileType
from archinstall.default_profiles.xorg import XorgProfile


class CinnamonProfile(XorgProfile):
	def __init__(self) -> None:
		super().__init__('Cinnamon', ProfileType.DesktopEnv)

	@property
	@override
	def packages(self) -> list[str]:
		return [
			'bibata-cursor-theme-bin',
			'blueman',
			'bluez-utils',
			'cinnamon',
			'cinnamon-translations',
			'engrampa',
			'firefox',
			'ghostty',
			'git',
			'gnome-keyring',
			'gnome-screenshot',
			'gnome-terminal',
			'gvfs',
			'gvfs-nfs',
			'gvfs-smb',
			'iso-flag-png',
			'materia-gtk-theme',
			'mintlocale',
			'nemo-fileroller',
			'nemo-preview',
			'nemo-share',
			'neo-candy-icons-git',
			'neovim',
			'pavucontrol',
			'system-config-printer',
			'wget',
			'xdg-user-dirs-gtk',
			'xed',
			'xfce4-terminal',
		]

	@property
	@override
	def default_greeter_type(self) -> GreeterType:
		return GreeterType.Sddm
