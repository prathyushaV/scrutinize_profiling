Filename:/opt/stack/new/nova/nova/api/openstack/wsgi.py
Methodname:_process_stack
1
           @coverage
           def _process_stack(self, request, action, action_args,
                              content_type, body, accept):
               """Implement the processing stack."""
       
               # Get the implementing method
+++++++        nova_value = 1
+++++++        if nova_value == 2:
>>>>>>             LOG.debug("nova boot is 2")
+++++++        elif nova_value == 1:
+++++++            LOG.debug("nova boot is 1")
+++++++        try:
+++++++            meth, extensions = self.get_method(request, action,
+++++++                                               content_type, body)
>>>>>>         except (AttributeError, TypeError):
>>>>>>             return Fault(webob.exc.HTTPNotFound())
>>>>>>         except KeyError as ex:
>>>>>>             msg = _("There is no such action: %s") % ex.args[0]
>>>>>>             return Fault(webob.exc.HTTPBadRequest(explanation=msg))
>>>>>>         except exception.MalformedRequestBody:
>>>>>>             msg = _("Malformed request body")
>>>>>>             return Fault(webob.exc.HTTPBadRequest(explanation=msg))
       
+++++++        if body:
>>>>>>             msg = _("Action: '%(action)s', body: "
>>>>>>                     "%(body)s") % {'action': action,
>>>>>>                                    'body': unicode(body, 'utf-8')}
>>>>>>             LOG.debug(logging.mask_password(msg))
+++++++        LOG.debug(_("Calling method '%(meth)s' (Content-type='%(ctype)s', "
                           "Accept='%(accept)s')"),
+++++++                  {'meth': str(meth),
+++++++                   'ctype': content_type,
+++++++                   'accept': accept})
       
               # Now, deserialize the request body...
+++++++        try:
+++++++            contents = {}
+++++++            if self._should_have_body(request):
                       #allow empty body with PUT and POST
>>>>>>                 if request.content_length == 0:
>>>>>>                     contents = {'body': None}
                       else:
>>>>>>                     contents = self.deserialize(meth, content_type, body)
>>>>>>         except exception.InvalidContentType:
>>>>>>             msg = _("Unsupported Content-Type")
>>>>>>             return Fault(webob.exc.HTTPBadRequest(explanation=msg))
>>>>>>         except exception.MalformedRequestBody:
>>>>>>             msg = _("Malformed request body")
>>>>>>             return Fault(webob.exc.HTTPBadRequest(explanation=msg))
       
               # Update the action args
+++++++        action_args.update(contents)
       
+++++++        project_id = action_args.pop("project_id", None)
+++++++        context = request.environ.get('nova.context')
+++++++        if (context and project_id and (project_id != context.project_id)):
>>>>>>             msg = _("Malformed request URL: URL's project_id '%(project_id)s'"
                           " doesn't match Context's project_id"
                           " '%(context_project_id)s'") % \
>>>>>>                     {'project_id': project_id,
>>>>>>                      'context_project_id': context.project_id}
>>>>>>             return Fault(webob.exc.HTTPBadRequest(explanation=msg))
       
               # Run pre-processing extensions
+++++++        response, post = self.pre_process_extensions(extensions,
+++++++                                                     request, action_args)
       
+++++++        if not response:
+++++++            try:
+++++++                with ResourceExceptionHandler():
+++++++                    action_result = self.dispatch(meth, request, action_args)
>>>>>>             except Fault as ex:
>>>>>>                 response = ex
       
+++++++        if not response:
                   # No exceptions; convert action_result into a
                   # ResponseObject
+++++++            resp_obj = None
+++++++            if type(action_result) is dict or action_result is None:
+++++++                resp_obj = ResponseObject(action_result)
>>>>>>             elif isinstance(action_result, ResponseObject):
>>>>>>                 resp_obj = action_result
                   else:
>>>>>>                 response = action_result
       
                   # Run post-processing extensions
+++++++            if resp_obj:
                       # Do a preserialize to set up the response object
+++++++                serializers = getattr(meth, 'wsgi_serializers', {})
+++++++                resp_obj._bind_method_serializers(serializers)
+++++++                if hasattr(meth, 'wsgi_code'):
>>>>>>                     resp_obj._default_code = meth.wsgi_code
+++++++                resp_obj.preserialize(accept, self.default_serializers)
       
                       # Process post-processing extensions
+++++++                response = self.post_process_extensions(post, resp_obj,
+++++++                                                        request, action_args)
       
+++++++            if resp_obj and not response:
+++++++                response = resp_obj.serialize(request, accept,
+++++++                                              self.default_serializers)
       
+++++++        if hasattr(response, 'headers'):
+++++++            if context:
+++++++                response.headers.add('x-compute-request-id',
+++++++                                     context.request_id)
       
+++++++            for hdr, val in response.headers.items():
                       # Headers must be utf-8 strings
+++++++                response.headers[hdr] = utils.utf8(str(val))
       
+++++++        return response
