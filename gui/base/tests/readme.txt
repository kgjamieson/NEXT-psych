BD Testing ReadMe
mantainer: Chris Fernandez, crfernandez@wisc.edu

Philosophy:
- "It's tested or it's broken"
- 100% "outside-in": all tests utilize a real web browser to simulate user behavior in each test scenario. Behavior is agnostic to implementation details.

Structure:
All 'Features' and 'Scenarios' for BD testing are defined in comments at the top of *.py test files.

Current Feature Tests:
create_proj_create_exp.py: tests a variety of project creation and deletion, experiment creation, staging, and running, and target upload scenarios.
valid_login_logout_test.py: tests authentication / login system. more scenarios needed but not yet available as development of alerts is in progress.
	Note: any file *_raw.html can be uploaded into Selenium IDE for faster browser testing. These have the same testing functionality as *.py counterpart.

TODOs:
1. HOSTNAME url is hard coded. This must be updated to your ec2 instance URL for tests to work. Need to dynamically populate these via PATH variables (denoted in Kevin's ec2 dev env setup instructions).
2. Line 101 create_proj_create_exp.py: directory path to animals.csv must be uniform on everyones test server. Use a relative PATH location of */next-frontend/next_frontend/base/tests/animals.csv to enable this.
3. Test user "fez_test" with pass "foo" used for all tests. Need some standardized way of creating and deleting a test user. This functionality will be added as soon as users can be deleted. Until then, create a test user "fez_test" with pass "foo".
4. Tests execution is slow. Move to 'headless' browser setup for faster tests.
5. Nose integration. Link these tests togather so that all can be executed with one command.