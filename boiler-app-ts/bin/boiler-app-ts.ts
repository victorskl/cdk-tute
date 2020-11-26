#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { BoilerAppTsStack } from '../lib/boiler-app-ts-stack';

const app = new cdk.App();
new BoilerAppTsStack(app, 'BoilerAppTsStack');
