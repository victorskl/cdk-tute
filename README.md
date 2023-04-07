# cdk-tute

AWS Cloud Development Kit (AWS CDK) tutes

- (blurb) https://aws.amazon.com/cdk/
- (source) https://github.com/aws/aws-cdk
- (this) https://docs.aws.amazon.com/cdk/latest/guide/home.html

**TL;DR**

- Alternate to [Terraform](https://github.com/victorskl/terraform-tute) or CloudFormation or [Ansible](https://github.com/victorskl/ansible-tute) for [IaC-ing](https://en.wikipedia.org/wiki/Infrastructure_as_code) **_specifically_** to AWS Cloud
- Written in TypeScript, hence, it is distributed as `cdk` CLI tool through Node/NPM/Yarn eco-system
- Use [jsii](https://github.com/aws/jsii) to support polyglot libraries, i.e. 
    - You write your IaC in general programming languages like Python or Java or TypeScript
    - Then, you use `cdk` CLI to run the code and deploy the infrastructure
    - This is the main contrast to the declarative [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) approach found in Terraform (`*.tf`) or CloudFormation (`*.json` or `*.yml`) or Ansible (`*.yml`)

**Getting Started**

- Install CLI
```
yarn global add cdk
yarn global upgrade cdk
which cdk
cdk version
```

- Hello CDK in Python
```
mkdir hello-cdk
cd hello-cdk
cdk init --list
cdk init sample-app --language=python --generate-only

pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest

cdk list
cdk synth
cdk diff
cdk deploy

aws sqs list-queues
aws sns list-topics
aws cloudformation list-stacks
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE
aws cloudformation get-template --stack-name hello-cdk > cfn_processed_tpl.json

cdk diff
cdk destroy

aws cloudformation list-stacks --stack-status-filter DELETE_COMPLETE
```

## Boilerplate

- Boiler App
```
mkdir boiler-app
cd boiler-app
cdk init app --language=python --generate-only
tree .
cdk list
cdk synth
cdk diff
```

- Boiler App in TypeScript
```
mkdir boiler-app-ts && cd boiler-app-ts
cdk init app --language=typescript --generate-only
tree .
yarn install
yarn run build
yarn run test
cdk list
cdk synth
cdk diff
```

- Boiler App in Java
```
mkdir boiler-app-java && cd boiler-app-java
cdk init app --language=java --generate-only
tree .
mvn compile
mvn test
mvn clean
mvn package
cdk list
cdk synth
```
