#!/bin/sh
PYTHONPATH=..:../xivo_restapi:../../xivo-dao/xivo-dao:../../xivo-acceptance:../../xivo-ws lettuce features/campaigns.feature --with-xunit --verbosity=3 --xunit-file=xunit-tests-campaigns.xml