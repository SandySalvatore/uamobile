# -*- coding: utf-8 -*-
from uamobile.base import UserAgent, Display

class SoftBankUserAgent(UserAgent):
    carrier = 'SoftBank'
    short_carrier = 'S'
    serialnumber = None

    def get_flash_version(self):
        """
        returns Flash Lite version.
        """
        from uamobile.data.flash.softbank import DATA

        if self.model.startswith('V'):
            model = self.model[1:]
        else:
            model = self.model

        try:
            return DATA[model]
        except KeyError:
            pass

        try:
            # for 831SHs, 830SHp, etc
            return DATA[model[:-1]]
        except KeyError:
            if self.vendor == 'MOT':
                # MOT-V980/80.2F.2E. MIB/2.2.1 Profile/MIDP-2.0 Configuration/CLDC-1.1
                return None
            else:
                return '2.0'
    flash_version = property(get_flash_version)

    def supports_cookie(self):
        """
        returns True if the device supports HTTP Cookie.
        For more information, see
        http://www2.developers.softbankmobile.co.jp/dp/tool_dl/download.php?docid=119
        """
        return self.is_3g() or self.is_type_w()

    def strip_serialnumber(self):
        """
        strip Device ID(Hardware ID)
        """
        if not self.serialnumber:
            return super(SoftBankUserAgent, self).strip_serialnumber()

        return self.useragent.replace('/SN%s' % self.serialnumber, '')

    def is_softbank(self):
        return True

    def is_vodafone(self):
        return True

    def is_jphone(self):
        return True

    def is_3g(self):
        return self._is_3g

    def is_type_c(self):
        """
        returns True if the type is C.
        """
        return not self._is_3g and (self.version.startswith('3.') or self.version.startswith('2.'))

    def is_type_p(self):
        """
        returns True if the type is P.
        """
        return not self._is_3g and self.version.startswith('4.')

    def is_type_w(self):
        """
        returns True if the type is W.
        """
        return not self._is_3g and self.version.startswith('5.')

    def get_jphone_uid(self):
        """
        returns the x-jphone-uid
        for the information about x-jphone-uid, see
        http://developers.softbankmobile.co.jp/dp/tool_dl/web/tech.php
        """
        try:
            return self.environ['HTTP_X_JPHONE_UID']
        except KeyError:
            return None
    jphone_uid = property(get_jphone_uid)

    def get_msname(self):
        return self.environ.get('HTTP_X_JPHONE_MSNAME')
    msname = property(get_msname)

    def get_smaf(self):
        return self.environ.get('HTTP_X_JPHONE_SMAF')
    smaf = property(get_smaf)

    def make_display(self):
        """
        create a new Display object.
        """
        try:
            width, height = list(map(int, self.environ.get('HTTP_X_JPHONE_DISPLAY', '').split('*', 1)))
        except ValueError:
            # x-jphone-display is absent, or invalid format
            width = None
            height = None

        # assuming that WSGI environment variable is always string if the key exists
        color_string = self.environ.get('HTTP_X_JPHONE_COLOR', '')
        color = color_string.startswith('C')

        try:
            depth = int(color_string[1:])
        except (ValueError, TypeError):
            depth = 0

        return Display(width=width, height=height, color=color, depth=depth)

    def get_java_info(self):
        import warnings
        warnings.warn("'java_info' is depracted. use 'info' instead", DeprecationWarning)
        return self.info
    java_info = property(get_java_info)
